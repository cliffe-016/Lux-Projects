from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.standard.operators.python import PythonOperator
import http.client
import pandas as pd
from sqlalchemy import create_engine, text
import json


def extract_gasprices(**kwargs):
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': "apikey 6ff03wNo6hslx7zqTGp7KY:4kJBtrc6HuLqHwCmC52hDd"
        }

    conn.request("GET", "/gasPrice/stateUsaPrice?state=WA", headers=headers)

    res = conn.getresponse()
    data = res.read()

    decoded_data = data.decode("utf-8")
    # return decoded_data

    kwargs['ti'].xcom_push(key='raw_gas_data', value=decoded_data)

def transform_gasprices(**kwargs):

    raw_gasprices = kwargs['ti'].xcom_pull(key='raw_gas_data', task_ids='extracting')
    # raw_gasprices = extract_gasprices()
    parsed_data = json.loads(raw_gasprices)

    cities_data = parsed_data['result']['cities']

    cities_df = pd.DataFrame(cities_data)

    cities_df = cities_df.rename(columns={ 'name':'cities'})

    cities_df = cities_df.drop(['lowername'], axis=1)

    json_data = cities_df.to_json(orient='records')

    kwargs['ti'].xcom_push(key='clean_gasdata', value=json_data)


def load_gasprices(**kwargs):
    data = kwargs['ti'].xcom_pull(key='clean_gasdata', task_ids='transforming')

    records = json.loads(data)
    df = pd.DataFrame(records)

    engine = create_engine('postgresql+psycopg2://postgres:12345@localhost:5432/postgres')

    df.to_sql('gas_prices', engine, if_exists='append', index=False)


with DAG(
    dag_id='gas_price_dag',
    start_date=datetime(2026, 4, 20),
    schedule =timedelta(minutes=5),
    catchup=False
) as dag:
    extract = PythonOperator(
        task_id='extracting',
        python_callable=extract_gasprices
    )

    transform = PythonOperator(
        task_id='transforming',
        python_callable=transform_gasprices
    )
    load = PythonOperator(
        task_id='loading',
        python_callable=load_gasprices
    )
    extract >> transform >> load
