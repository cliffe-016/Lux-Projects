from src.spark_utils import get_spark_session
from src.transforms import clean_orders, clean_items, clean_customers, enrich_orders, window_metrics, enrich_returns
import src.config as config

def main():
    # Initialize Spark Session
    print("Starting E-commerce Pipeline...")
    spark = get_spark_session()

    # Read raw data
    customers_raw = spark.read.csv(config.customers, header=True)
    items_raw = spark.read.csv(config.items, header=True)
    orders_raw = spark.read.csv(config.orders, header=True)
    returns_raw = spark.read.csv(config.returns, header=True)

    # Apply transformations
    print("Executing transformations...")
    customers_clean = clean_customers(customers_raw)
    items_clean = clean_items(items_raw)
    orders_clean = clean_orders(orders_raw)

    # Enrich the data
    enriched_df = enrich_orders(customers_clean, orders_clean, items_clean)
    enriched_df = window_metrics(enriched_df)

    # Extract the dictionary of dataframes from the returns function
    returns_results = enrich_returns(enriched_df, returns_raw)
    final_enriched_df = returns_results["final_enriched_df"]
    return_rates_df = returns_results["return_rates"]
    top_10_refunds_df = returns_results["top_10_refunds"]

    # Output and Partitioning
    print("Writing outputs to disk...")

    final_enriched_df.write \
        .mode("overwrite") \
        .partitionBy("order_year", "order_month") \
        .parquet(config.data_output)

    # Write aggregated summary tables to CSV
    return_rates_df.write \
        .mode("overwrite") \
        .csv(config.return_rates, header=True)
    
    top_10_refunds_df.write \
        .mode("overwrite") \
        .csv(config.top_refunds, header=True)

    print("Spark transformations complete")

if __name__ == "__main__":
    main()
