from massive import RESTClient
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import time

# Write ETL logic firsst
def extract(**kwargs):
    client = RESTClient("LKnpEkBqcVOJhkcOwMtHEDsJmuUMpliY")

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
    
    # Rate limting error to elminate 429 error
    time.sleep(2)
    # Convert list to dataframe first to flatten the list
    raw_df = pd.DataFrame(data)
    
    # Convert to json
    raw_data = json.loads(raw_df.to_json(orient="records"))

    kwargs["ti"].xcom_push(key="raw_json", value=raw_data)

def transform(**kwargs):
    data_transform = kwargs["ti"].xcom_pull(task_ids="extract", key="raw_json")
    df_transform = pd.DataFrame(data_transform)
    # Rename date column
    df_transform = df_transform.rename(columns={"from_":"date"})
    # Drop none valued column
    df_transform = df_transform.drop(["otc"], axis=1) 
    # Add price change column
    df_transform["price_change"] = df_transform["close"] - df_transform["open"]

    transformed_data = json.loads(df_transform.to_json(orient="records"))
    kwargs["ti"].xcom_push(key="transformed_json", value=transformed_data)

def load(**kwargs):
    transformed_data = kwargs["ti"].xcom_pull(task_ids="transform", key="transformed_json")
    # convert transformed data to df
    df_load = pd.DataFrame(transformed_data)

    # Define sqlalchemy engine
    engine = create_engine("postgresql+psycopg2://lux_user:1234@127.0.0.1:5432/massive_db")

    # Load
    df_load.to_sql("tech_stocks", con=engine, if_exists="append", index=False)
    print("Rows:", len(df_load), "loaded")


# Define dag arguments
with DAG(
    "cliffe_stocks_dag_ops",
    start_date=datetime(2026, 4, 24),
    schedule='@hourly',
    catchup=False,
    max_active_runs=1
    ) as dag:
        task_extract = PythonOperator(
            task_id="extract_data", 
            python_callable=extract)

        task_transform = PythonOperator(
            task_id="transform_data",
            python_callable=transform)

        task_load = PythonOperator(
            task_id="load_data",
            python_callable=load)


        task_extract >> task_transform >> task_load
