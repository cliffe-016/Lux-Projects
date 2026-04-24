from massive import RESTClient
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from airflow.sdk import dag, task
from datetime import datetime, timedelta
import json

# Define dag arguments
@dag(
    start_date=datetime(2026, 4, 24),
    schedule='@hourly',
    catchup=False
    )

# Define dag id
def cliffe_stocks_dag():
    @task()
    def extract():
        client = RESTClient("lppjfqABG22zKmPuspOyep56wMdB0772")

        # Store companies in a list
        companies = ["AAPL", "GOOG", "TSLA", "AMZN", "NFLX"]
        data = []

        # Iterate throguh companies list to extract data
        for ticker in companies:
            request = client.get_daily_open_close_agg(
                ticker,
                "2025-04-22",
                adjusted="true",
            )
            data.append(request)

        # Convert list to dataframe first to flatten the list
        raw_df = pd.DataFrame(data)
        
        # Convert to json
        raw_data = json.load(raw_df.to_json(orient="records"))

        return raw_data

    @task()
    def transform(raw_data):
        df_transform = extract()
        
        # Rename date column
        df_transform = df_transform.rename(columns={"from_":"date"})
        # Drop none valued column
        df_transform = df_transform.drop(["otc"], axis=1)   
        # Add price change column
        df_transform["price_change"] = df_transform["close"] - df_transform["open"]

        transformed_data = json.loads(df_transform.to_json(orient="records"))
        return transformed_data

    @task()
    def load(transformed_data):
        # convert transformed data to df
        df_load = pd.DataFrame(transformed_data)

        # Define sqlalchemy engine
        engine = create_engine("postgresql+psycopg2://lux_user:1234@127.0.0.1:5432/massive_db")

        # Load
        df_load.to_sql("tech_stocks", con=engine, if_exists="append", index=False)
        print("Rows:", len(df_load), "loaded")

    raw_data=extract()
    transformed_data = transform(raw_data)
    load(transformed_data)

cliffe_stocks_dag()
