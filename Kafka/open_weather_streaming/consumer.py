from kafka import KafkaConsumer
import json
from cassandra.cluster import Cluster
import pandas as pd
from datetime import datetime

consumer = KafkaConsumer(
    'weather-info',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda d: json.loads(d.decode('utf-8'))
    )


# Connect to Database
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
print("Database connection successful\n")

# Create database
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS weather_info
    WITH replication = {
        'class': 'SimpleStrategy',
        'replication_factor': 1
        }
    """)
session.set_keyspace('weather_info')
print("\nDatabase created")

# Create table
session.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id int PRIMARY KEY,
        sunrise timestamp,
        sunset timestamp,
        weather_id int,
        visibility int,
        status_code int,
        longitude double,
        latitude double,
        timezone text,
        temp double,
        temp_feels_like double,
        temp_min double,
        temp_max double,
        pressure int,
        humidity int,
        sea_level int,
        ground_level int,
        wind_speed double,
        wind_direction int,
        cloud_percentage int,
        city text,
        main_weather text,
        weather_description text,
        base text,
        country text
    )
""")
print("Table created successfully\n")

insert_query = session.prepare("""
    INSERT INTO weather_data (
        id, sunrise, sunset, weather_id, visibility, status_code, longitude, latitude, 
        timezone, temp, temp_feels_like, temp_min, temp_max, pressure, humidity, 
        sea_level, ground_level, wind_speed, wind_direction, cloud_percentage, 
        city, main_weather, weather_description, base, country
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
""")

print("\nWaiting for weather data...")

for message in consumer:
    raw_data = message.value
    print(f"Received: {raw_data}\n")
    
    try:
        # Flatten the data
        df = pd.json_normalize([raw_data])

        # Flatten the nested 'weather' column and add column prefixes
        data_weather = pd.json_normalize(raw_data, record_path=['weather'])
        df = df.drop(columns=['weather']).join(data_weather.add_prefix('weather_'))

        # Convert time columns from integer to timestamps
        time_columns = ['dt', 'sys.sunrise', 'sys.sunset']
        for col in time_columns:
            df[col] = pd.to_datetime(df[col], unit='s', utc=True)

        # Convert unix timestamps
        unix_to_dt = lambda t: datetime.fromtimestamp(t) if t else None

        # Convert timezone columns to timezone
        df['timezone'] = pd.to_timedelta(df['timezone'], unit='s').astype(str) # Convert to string for Cassandra

        # Define dictionary variables from the json data to match database colunms with json keys
        weather = raw_data.get('weather', [{}])[0]
        main_data = raw_data.get('main', {})
        sys_data = raw_data.get('sys', {})
        coord = raw_data.get('coord', {})
        wind = raw_data.get('wind', {})
        clouds = raw_data.get('clouds', {})

        # Load the data
        session.execute(insert_query, (
            raw_data.get('id'),
            unix_to_dt(sys_data.get('sunrise')),
            unix_to_dt(sys_data.get('sunset')),
            weather.get('id'),
            raw_data.get('visibility'),
            raw_data.get('cod'),
            coord.get('lon'),
            coord.get('lat'),
            str(raw_data.get('timezone')),
            main_data.get('temp'),
            main_data.get('feels_like'),
            main_data.get('temp_min'),
            main_data.get('temp_max'),
            main_data.get('pressure'),
            main_data.get('humidity'),
            main_data.get('sea_level'),
            main_data.get('grnd_level'),
            wind.get('speed'),
            wind.get('deg'),
            clouds.get('all'),
            raw_data.get('name'),
            weather.get('main'),
            weather.get('description'),
            raw_data.get('base'),
            sys_data.get('country')
            ))
        print("\nSuccessfully inserted data\n")

    except Exception as e:
        print(f"Error processing data: {e}")


