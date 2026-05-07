import psycopg2
import pandas as pd
from transform import transform_weather
import os 
from dotenv import load_dotenv

load_dotenv()

def load_weather():
    data = transform_weather()
    # Define database connection string
    conn = psycopg2.connect(
        host=os.get_env("HOST"),
        dbname=os.get_env("DBNAME"),
        user=os.get_env("user"),
        password=os.get_env("pass"),
        port=os.get_env("port")
        )
    cur = conn.cursor()
    
    # Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nairobi(
            id INT PRIMARY KEY,--id
            city TEXT,--name
            status_code INT,--cod
            longitude FLOAT,--coord.lon
            latitude FLOAT,--coord.lat
            timezone INTERVAL,--timezone
            temp FLOAT,--main.temp
            temp_feels_like FLOAT,--main.feels_like
            temp_min FLOAT,--main.temp_min
            temp_max FLOAT,--main.temp_max
            pressure INT,--main.pressure
            humidity INT,--main.humidity
            sea_level INT,--main.sea_level
            ground_level INT,--main.grnd_level
            wind_speed FLOAT,--wind.speed
            wind_direction INT,--wind.deg
            cloud_percentage INT,--clouds.all
            country TEXT,--sys.country
            sunrise TIMESTAMPTZ,--sys.sunrise
            sunset TIMESTAMPTZ,--sys.sunset
            weather_id INT,--weather_id
            main_weather TEXT,--weather_main
            weather_description TEXT,--weather_description
            base TEXT,--base
            visibility INT,--visibility
            time_now TIMESTAMPTZ --dt
            );
        """
    )
    for index, row in data.iterrows(): # iterrows for iterating through dataframes
        cur.execute("""
            INSERT INTO nairobi(
                id,--id
                city,--name
                status_code,--cod
                longitude,--coord.lon
                latitude,--coord.lat
                timezone,--timezone->timestamp
                temp,--main.temp
                temp_feels_like,--main.feels_like
                temp_min,--main.temp_min
                temp_max,--main.temp_max
                pressure,--main.pressure
                humidity,--main.humidity
                sea_level,--main.sea_level
                ground_level,--main.grnd_level
                wind_speed,--wind.speed
                wind_direction,--wind.deg
                cloud_percentage,--clouds.all
                country,--sys.country
                sunrise,--sys.sunrise->timestamp
                sunset,--sys.sunset->timestamp
                weather_id,--weather_id
                main_weather,--weather_main
                weather_description,--weather_description
                base,--base
                visibility,--visibility
                time_now --dt->timestamp
                )
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                    )
            """, (
                row['id'],                 # id
                row['name'],               # city
                row['cod'],                # status_code
                row['coord.lon'],          # longitude
                row['coord.lat'],          # latitude
                row['timezone'],           # timezone interval string
                row['main.temp'],          # temp
                row['main.feels_like'],    # temp_feels_like
                row['main.temp_min'],      # temp_min
                row['main.temp_max'],      # temp_max
                row['main.pressure'],      # pressure
                row['main.humidity'],      # humidity
                row['main.sea_level'],     # sea_level
                row['main.grnd_level'],    # ground_level
                row['wind.speed'],         # wind_speed
                row['wind.deg'],           # wind_direction
                row['clouds.all'],         # cloud_percentage
                row['sys.country'],        # country
                row['sys.sunrise'],        # sunrise
                row['sys.sunset'],         # sunset
                row['weather_id'],         # weather_id (flattened from weather list)
                row['weather_main'],       # main_weather (flattened from weather list)
                row['weather_description'], # weather_description (flattened from weather list)
                row['base'],               # base
                row['visibility'],         # visibility
                row['dt']
                ))
    conn.commit()
    cur.execute("SELECT * FROM nairobi ORDER BY time_now DESC LIMIT 1;")
    print("Data loaded successfully!: \n", cur.fetchone())

    cur.close()
    conn.close()

