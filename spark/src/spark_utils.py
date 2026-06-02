from pyspark.sql import SparkSession

def spark_session(app_name="E-commerce Pipeline"):
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    return spark
