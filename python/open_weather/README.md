# Open Weather ETL Pipeline

A Python-based ETL (Extract, Transform, Load) pipeline built as a learning project at LuxDevHQ to practice data engineering concepts. This project extracts live weather data from the OpenWeather API, transforms the nested JSON structures into a clean dataframe using Pandas, and loads the data into a local PostgreSQL database.

## Project Architecture

The pipeline follows a standard ETL structure:

1. **Extract (`extract.py`)**: Connects to the OpenWeather API to retrieve real-time weather data for Nairobi, Kenya. 
2. **Transform (`transform.py`)**: Takes the extracted data, normalizes nested JSON fields (specifically the `weather` array), renames columns with appropriate prefixes to avoid conflicts and converts the utc timestamps before database ingestion.
3. **Load (`load.py`)**: Connects to a local PostgreSQL database using `psycopg2` and loads the transformed data into the `open_weather` database.
4. **Orchestration (`main.py`)**: The entry point that runs the extraction, transformation, and loading steps sequentially.

## Tech Stack

* **Language**: Python 3.12+
* **Data Manipulation**: Pandas
* **API Requests**: Requests
* **Database**: PostgreSQL, Psycopg2, SQLAlchemy
* **Package Management**: `uv` 

## Installation
Clone this repository to your local machine.
Navigate to the project directory.
Install the dependencies using uv:
```
uv sync
```

### Setup
A local PostgreSQL database is created and accessed with the matching credentials specified in `load.py`:

```sql
CREATE DATABASE open_weather;
CREATE USER lux_user WITH PASSWORD '1234';
GRANT ALL PRIVILEGES ON DATABASE open_weather TO lux_user;
```

## Workflow
* Accessed the Open Weather API using the `requests` library, converted the data to json and flattened it using `json_normalize` as it contained list, dictionaries and lists of dictionaries. I then saved it to a variable as it's already converted to a dataframe with `json_normlaize`.
* Transformed the `weather` column from a list of dictionaries, using the same pandas method `json_normalize` but passed `record_path=['weather']` to explicitly flatten the `weather` column. I also used the json data instead of the dataframe to avoid a `TypeError`(`json_normalize` expects a list). I then joined the two dataframes, ensuring the flattened columns are saved with the prefix `weather_id` to avoid a `ValueError`.
* The data was then loaded to a postgres database using psycopg2.

## Key Learnings & Concepts Applied
**Interacting with APIs:** Handling requests and processing raw JSON responses.

**Data Flattening:** Using `pd.json_normalize` with `record_path` to unpack nested data and dictionaries into a format suitable for pandas Dataframes.

**Database Connections:** Connecting to PostgreSQ and executing queries in python.

**Modularization:** Separating ETL processes into separate scripts rather than a single file.
