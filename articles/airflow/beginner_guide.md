# A Beginner's Guide to Apache Airflow 3
If encountered the terms _orchestration_  or _apache airflow_ and have no clue what they mean, this article will provide clarity and a basic understanding of these concepts.
_What is orchestration?_ This is a core process of data operations(DataOps) that manages data tasks (e.g extract, transform, load for etl pipelines) such that they run in the **correct order**, at the **right time**.
It simple ensures that data processing tasks are sequenced, so that when one task (transformation) depends on the outcome of another (extraction), the latter (extraction) runs first. To achieve this, data engineers often use DAGs (Directed Acyclic Graphs).
_What is a DAG?_ A Directed Acyclic Graph (DAG) is a model that contains all the _tasks_ to be run. It is **Directed** meanig tasks have a specific direction; **Acyclic** meaning it has no circular dependencies (extraction cannot depend on transformation if transformation depends on extraction); **Graph** meaning a collection of tasks (nodes) connected by dependencies (edges).
_What is a Task?_ This is a step in a DAG that describes a single unit of work.

So, to orchestrate you have to define a DAG object that contains one or more tasks to orchestrate a data pipeline. How would you do this? You use an orchestration tool like Apache Airflow which is an open-source tool for defining, scheduling and monitoring batch-oriented pipelines. An Airflow instance contains the following main components:
* The **Scheduler** submits tasks to the executor and triggers scheduled workflows.
* A **DAG processor** reads DAG files and organizes them in the metadata database.
* The **Webserver** which is the airflow User Interface for inspecting, trigerring and debugging the behaviour of dags and tasks.
* A dedicated folder of **DAG files** which contains the dag and is read by the scheduler to figure which tasks to run and when to tun them.
* The **Metadata Database** stores the state of tasks, dags and avriables




