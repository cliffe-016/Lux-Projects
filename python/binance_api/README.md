# Binance API ETL Pipeline
This is an ETL (Extract, Transform, Load) learning project designed to ingest, process and store cryptocurrency market data. This pipeline fetches 7-day rolling window ticker data for Bitcoin (BTC/USDT) from the public Binance Data API, processes the raw timestamps into a database-friendly format and loads the data into a local PostgreSQL database.

## How This Project Was Built

This project is structured into the three distinct modules in ETL:

### 1. Extract (`extract.py`)
The pipeline begins by interacting with the Binance API endpoint (`http://data-api.binance.vision/api/v3/ticker`). 
* The `requests` library is used to send a GET request parameterized for the `BTCUSDT` symbol and a `7d` window size. 
* The raw JSON response is retrieved and immediately flattened into a dataframe using Pandas' `json_normalize()` function.

### 2. Transform (`transform.py`)
This step transmforms the data before load. 
* The `openTime` and `closeTime` columns, which the Binance API provides as reandom integers are converted to unix timestamps in milliseconds.
* This column (`pd.to_datetime`) is also converted from raw integers into timezone-aware (UTC) Python datetime objects, ensuring chronological data is accurately stored and easily queried later.

### 3. Load (`load.py`)
The final step handles database ingestion using `psycopg2`.
* It connects to a local PostgreSQL database (`binance`).
* A `CREATE TABLE IF NOT EXISTS` statement ensures the `ticker` table is created with the correct schema (using `TIMESTAMPTZ` for the transformed time columns and `FLOAT` for price/volume metrics).
* The transformed dataFrame is iterated over, and the data is inserted row by row into the database. Finally, a sample query runs to confirm the most recent entry was successfully loaded.

## Tech Stack

* **Language**: Python 3.12+
* **Data Processing**: Pandas
* **API Interactions**: Requests
* **Database**: PostgreSQL, Psycopg2
* **Package Management**: `uv` 

## Prerequisites

To run this project locally, you will need:
* Python 3.12 or higher
* A local instance of PostgreSQL running on port `5432`

### Database Setup
Before running the pipeline, set up the required PostgreSQL database and user credentials. You can execute the following in your `psql` terminal:

```sql
CREATE DATABASE binance;
CREATE USER lux_user WITH PASSWORD '1234';
GRANT ALL PRIVILEGES ON DATABASE binance TO lux_user;
```

### Installation
```
uv sync
```

### Usage
```
uv run main.py
```        

### Concepts Learned
**1. ETL Architecture**
Instead of writing a single script, the logic is separated into distinct extract.py, transform.py, and load.py modules also separating points of failure.

**2. REST APIs**
Interacted with two different live data sources, and learned how to use parameters (like BTCUSDT and the 7d window size for Binance) to tailor the data payload.

**3. Data Transformation with Pandas**
* Flattening Nested Data: Using pd.json_normalize() to unpack nested JSON arrays (like the weather descriptions) into a dataframe.
* Datetime Standardization: Handled Unix timestamps in milliseconds and successfully converted them into  (UTC) datetime objects. 

