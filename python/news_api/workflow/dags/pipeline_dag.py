import sys
import os
# Dynamically get the current directory
current_file_path = os.path.realpath(__file__)
dags_folder = os.path.dirname(current_file_path)
airflow_folder = os.path.dirname(dags_folder)
project_root = os.path.dirname(airflow_folder)

# Inject the paths dynamically
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'venv/lib/python3.12/site-packages'))

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
from main import main

with DAG(
    dag_id="news_pipeline",
    schedule='@daily',
    start_date=datetime(2026, 4, 16),
    catchup=False,
    max_active_runs=1
) as dag:
    task_news = PythonOperator(
        task_id='news_pipeline',
        python_callable=main
        )
