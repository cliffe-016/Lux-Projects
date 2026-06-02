from pyspark.sql import Window
import pyspark.sql.functions as F

def clean_items(df):
    """Drops duplicate items and removes rows with no order_id."""
    return df.dropDuplicates(['item_id']).filter(F.col("order_id").isNotNull())

def clean_orders(df):
    """Drops duplicate orders and removes rows with no order_id."""
    return df.dropDuplicates(['order_id']).filter(F.col("order_id").isNotNull())

def clean_customers(df):
    """Cleans the data"""
    df = df.filter(
        F.expr("try_to_date(signup_date, 'MM/dd/yyyy')").isNotNull() | 
        F.expr("try_to_date(signup_date, 'yyyy-MM-dd')").isNotNull()
    )
    df = df.select(
        F.col("customer_id").cast("string"), 
        F.coalesce(
            F.expr("try_to_date(signup_date, 'MM/dd/yyyy')"),
            F.expr("try_to_date(signup_date, 'yyyy-MM-dd')")
        ).alias("signup_date"), 
        F.col("country").cast("string"), 
        F.lower(F.col("customer_tier")).alias("customer_tier"), 
        F.col("email").cast("string")
    )
    return df.dropDuplicates(['customer_id']).filter(F.col("customer_id").isNotNull())

def enrich_orders(customers_df, orders_df, items_df):
    """Joins tables and calculates the net amount"""
    customer_orders_df = customers_df.join(orders_df, on="customer_id", how="inner")
    enriched_df = customer_orders_df.join(items_df, on="order_id", how="inner")
    
    enriched_df = enriched_df.withColumn(
        "net_amount",
        F.col("total_amount") * (1 - F.col("discount_pct") / 100)
    )
    # Add partition columns for the final Parquet write
    enriched_df = enriched_df.withColumn("order_year", F.year("order_date")) \
                             .withColumn("order_month", F.month("order_date"))
    return enriched_df

def window_metrics(enriched_df):
    """Performs window functions """
    # Lifetime spend rank per country
    window_cust = Window.partitionBy("customer_id")
    window_rank = Window.partitionBy("country").orderBy(F.desc("lifetime_spend"))
    
    df = enriched_df.withColumn("lifetime_spend", F.sum("net_amount").over(window_cust))
    df = df.withColumn("country_spend_rank", F.dense_rank().over(window_rank))
    
    # 7-day rolling order count
    seven_days_sec = 604800
    df = df.withColumn("order_time_sec", F.col("order_date").cast("timestamp").cast("long"))
    rolling_window = Window.partitionBy("customer_id").orderBy("order_time_sec").rangeBetween(-seven_days_sec, Window.currentRow)
    df = df.withColumn("7_day_rolling_orders", F.count("order_id").over(rolling_window))
    
    # Category revenue share per month
    df = df.withColumn("order_month_start", F.trunc("order_date", "month"))
    window_month = Window.partitionBy("order_month_start")
    window_cat_month = Window.partitionBy("order_month_start", "category")
    
    df = df.withColumn("total_monthly_revenue", F.sum("net_amount").over(window_month))
    df = df.withColumn("category_monthly_revenue", F.sum("net_amount").over(window_cat_month))
    df = df.withColumn("category_revenue_share", F.col("category_monthly_revenue") / F.col("total_monthly_revenue"))
    
    return df

def enrich_returns(enriched_df, returns_df):
    """Enriches return dataframe."""
    joined_returns_df = enriched_df.join(returns_df, on="order_id", how="left")
    
    # Add exceeds order flag
    joined_returns_df = joined_returns_df.withColumn(
        "refund_exceeds_order",
        F.col("refund_amount") > F.col("net_amount")
    )
    
    # Calculate Return Rate
    return_rates_df = joined_returns_df.groupBy("category", "customer_tier").agg(
        F.count("order_id").alias("total_orders"),
        F.count("return_id").alias("total_returns")
    ).withColumn("return_rate", F.col("total_returns") / F.col("total_orders"))
    
    # Top 10 Customers by Refund
    top_10_refunds_df = joined_returns_df.groupBy("customer_id").agg(
        F.sum("refund_amount").alias("total_refunded")
    ).orderBy(F.desc("total_refunded")).limit(10)
    
    return {
        "final_enriched_df": joined_returns_df,
        "return_rates": return_rates_df,
        "top_10_refunds": top_10_refunds_df
    }
