# A Beginner's Guide to Apache Airflow 3
If the terms _orchestration_ or _Apache Airflow_ sound like intimidating industry jargon, this article will help you cut through the noise and understand the basics.
So what exactly is _data orchestration?_ In DataOps (Data Operations), it is the underlying system that manages data workflows (such as ETL pipelines) to ensure tasks run at the right time and in the correct sequence.
For example, if data transformation depends on extraction, orchestration makes sure the extraction process runs to completion first.
_What is a DAG?_ A DAG is a model that contains all the _tasks_ to be run. It stands for:
* **Directed** meaning tasks have a specific direction.
* **Acyclic** meaning it has no circular dependencies (extraction cannot depend on transformation if transformation depends on extraction).
* **Graph** meaning a collection of tasks (nodes) connected by dependencies (edges).
_What is a Task?_ This is a step in a DAG that describes a single unit of work.

So, to orchestrate you have to define a DAG object that contains one or more tasks to orchestrate a data pipeline. How would you do this? You use an orchestration tool like Apache Airflow which is an open-source tool for defining, scheduling and monitoring batch-oriented pipelines. An Airflow instance contains the following main components:
* The **Scheduler** submits tasks to the executor and triggers scheduled workflows.
* A **DAG processor** reads DAG files and organizes them in the metadata database.
* The **Webserver** is the Airflow User Interface for inspecting, triggering and debugging the behaviour of DAGs and tasks.
* A dedicated folder of **DAG files** which contains the DAG and is read by the scheduler to figure out which tasks to run and when to run them.
* The **Metadata Database** stores the state of tasks, DAGs and variables.

At this point you might be asking yourself, _Why not just use cron jobs?_ Well, think of cron jobs as an alarm clock and Airflow as a project manager. Cron just runs your script at a certain time with no regard for the task's dependencies. Say you schedule extract.py for 12:00 AM and transform.py for 1:30 AM. If extraction takes 40 minutes, Cron will blindly trigger the transformation at 1:30 AM, leading to corrupted data. Airflow, acting as a project manager, understands this dependency; it waits patiently for extraction to finish and will automatically retry the task if it times out.
To make sense of all this jargon, below is an example of a simple DAG:
```
from airflow.sdk import DAG 
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta 

# Step 1: Define your Python functions 
def my_function():
    # Your logic here
    pass

# Step 2: Set default arguments
default_args = {
    'owner': 'your_name',
    'depends_on_past': False,           # don't wait for previous DAG runs
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'retries': 1,                       # retry once if it fails
    'retry_delay': timedelta(minutes=5)
}

# Step 3: Create DAG object
with DAG(
    dag_id='template_dag',              # unique DAG identifier
    default_args=default_args,          # default args defined above
    description='Template for new DAGs',# DAG description
    schedule_interval='@daily',         # frequency of execution (you could use cron expressions for granularity)
    catchup=False,                      # don't run for previous dates
    max_active_runs=1                   # run one instance at a time
)

# Step 4: Define tasks
task1 = PythonOperator(
    task_id='python_task',          # unique task identifier
    python_callable=my_function,    # Python function to be executed
    dag=dag
)

task2 = BashOperator(
    task_id='bash_task',
    bash_command='echo "Hello World"',
    dag=dag
)

# Step 5: Set dependencies
task1 >> task2
```

As you can see from the example above, we use Python to declare tasks and their dependencies. These instructions are then interpreted by the orchestration engine and run sequentially using the available resources. This is what data engineers refer to as _Workflow As Code_. In the example, the DAG is defined using traditional operators as in `PythonOperator` and `BashOperator`.
However, this is not the only method used; Airflow has a built-in 'TaskFlow API' that defines DAGs using Python decorators, which  makes it easier to pass data between DAGs. Here is an example of a simple ETL pipeline:
```
import json
from airflow.decorators import dag, task
from pendulum import datetime

# 1. Define the DAG using the @dag decorator
@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["example", "taskflow"],
)
def taskflow_etl_pipeline():

    # 2. Extract: Task returns a dictionary 
    @task()
    def extract():
        data_string = '{"1001": 30.5, "1002": 28.2, "1003": 31.1}'
        return json.loads(data_string)

    # 3. Transform: Receives data directly from the upstream task
    @task()
    def transform(raw_data: dict):
        total_value = sum(raw_data.values())
        return {"total": total_value, "count": len(raw_data)}

    # 4. Load: Final task to "load" or print the data
    @task()
    def load(processed_data: dict):
        print(f"Loading data: Total value is {processed_data['total']}")

    # 5. Define dependencies by calling the functions
    raw_data = extract()
    summary = transform(raw_data)
    load(summary)

# Instantiate the DAG
taskflow_etl_pipeline()

```

How can you tell if your DAG runs? Use the `airflow dags list` command to check if it's been parsed by the scheduler. Alternatively, you could check the user interface at `localhost:8080`. To ensure configuration errors are avoided use the following link for a step-by-step guide on installation and setup:
[Step by step guide on how to Install and Setup Apache Airflow](https://www.notion.so/Setting-up-Airflow-3-0-353cf979b71d80ffb7c6cd6f9d8fdc64?source=copy_link)

## Best Practices
As your workflows grow in complexity, adhering to a few core principles will save you from scheduling nightmares and data corruption. Let's look at some of them:
**1. Idempotency:** A task should return the exact same outcome whether it is run once, twice or a hundred times for the same execution date.
**2. Atomicity:** Each task should perform one defined operation. This ensures modularity. If the transformation phase fails, you only need to retry that specific task instead of re-fetching all your raw data from the source.
**3. Encapsulation:** Only define DAG structure at the top level. If you put heavy data processing, API calls or database queries in the global scope of your file (outside of the actual task definitions), the scheduler will execute that code every single time it parses the file. This will crash your Airflow instance.


## Summary
To sum everything up, Apache Airflow might seem intimidating at first, but at its core, it is simply a tool designed to bring order to chaos. By embracing orchestration, you transform isolated, manually run scripts into reliable, automated data pipelines. To recap the key takeaways:
* **Data Orchestration** is essential to data pipelines, it ensures your data tasks run in the right sequence and at the right time.
* **DAGs are the blueprint**, they provide a map of your tasks and dependencies, ensuring no task runs out of order.
* **Airflow does the heavy lifting** by handling the logistics of executing and monitoring your tasks so you can focus on the logic.
* **Workflow as Code:** Whether you use traditional operators or the modern, Pythonic TaskFlow API, you have the flexibility to define complex pipelines.

