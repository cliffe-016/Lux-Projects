from massive import RESTClient
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from airflow.sdk import dag, task
from datetime import datetime, timedelta
import json

@dag(
    start_date=datetime(2026, 4, 23),
    schedule='@daily',
    catchup=False
    )

def pipeline_dag():
    @task()
    def extract():
        client = RESTClient("lppjfqABG22zKmPuspOyep56wMdB0772")

        tickers = []
        for t in client.list_tickers(
	        type="FUND",
	        market="stocks",
	        active="true",
	        order="asc",
	        limit="100",
	        sort="ticker",
	        ):
            tickers.append(t)

        df = pd.DataFrame(tickers)
        raw = json.loads(df.to_json(orient="records"))
        return raw

    @task()
    def transform(raw):
        df = pd.DataFrame(raw)

        transformed_data = df.drop(['currency_symbol', 'base_currency_symbol', 'base_currency_name', 'delisted_utc', 'source_feed'], axis=1)
        transformed_data = json.loads(transformed_data.to_json(orient="records"))
        return transformed_data

    @task()
    def load(data):
        data = pd.DataFrame(data)
        engine = create_engine("postgresql+psycopg2://lux_user:1234@127.0.0.1:5432/massive_db")
        data.to_sql("stocks", con=engine, if_exists="append", index=False)
        print("Rows:", len(data), "loaded")

    raw = extract()
    transformed_data = transform(raw)
    load(transformed_data)

pipeline_dag()


