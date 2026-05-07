# Crypto Data ETL Pipeline 

This project is a containerized Extract, Transform, Load (ETL) pipeline that fetches live cryptocurrency market data from Coinpaprika API, cleans and processes the data, and loads it into a PostgreSQL database.


##  Tech Stack
Python 3 (Data extraction and processing)

Pandas (Data transformation and normalization)

PostgreSQL (Data storage)

SQLAlchemy & psycopg2 (Database connection and ORM)

Docker & Docker Compose (Containerization)

## Project Structure
**coins_etl.py:** The main Python script that runs the ETL process.

**Dockerfile:** Defines the Python environment and installs dependencies.

**docker-compose.yaml:** Containerizes the postgres database and the ETL container, handling network connections between them.

**requirements.txt:** Lists the Python dependencies required for the script.

**test.ipynb:** A Jupyter Notebook used for initial API testing and data exploration

**.env:** Stores secure environment variables

## Prerequisites
To run this project, you will need to have the following installed on your machine:

* Docker

* Docker Compose

## Setup & Execution
### 1. Create your Environment Variables
For security, database credentials are stored in a .env file in the root directory of the project:
```Ini, TOML
DB_USER=postgres
DB_PASS=your_secure_password
DB_HOST=postgres
DB_PORT=5432
DB_NAME=paprika
```
(Note: DB_HOST must remain postgres so the Docker containers can communicate over the internal Docker network).

### 2. Build and Run the Pipeline
Open your terminal, navigate to the project directory, and run the following command to build the images and spin up the containers in detached mode:

```Bash
sudo docker compose up --build -d
```

### 3. Verify the Data
You can check the logs of the ETL container to ensure the script ran successfully:

```Bash
sudo docker logs crypto_etl
```

To view the data directly inside the PostgreSQL database, you can execute into the running database container:

```Bash
sudo docker exec -it postgres bash
```
Then log into the PostgreSQL prompt:

```Bash
psql -U postgres -d paprika
```
And run a test query:

```SQL
SELECT * FROM coins_data;
```
### 4. Shutting Down
To stop the containers and clean up the network, run:

```Bash
sudo docker compose down
```

## Data Schema
The output table coins_data contains the following columns extracted from the API:

`coin_name`: The full name of the cryptocurrency coin.

`coin_symbol`: The ticker symbol (e.g., BTC).

`last_updated`: Timestamp of the latest data point.

`price`: The current price in USD.

`percent_change_24h`: The percentage change in price over the last 24 hours.
