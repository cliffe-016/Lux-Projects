import psycopg2
from transform import transform_btc
import os
from dotenv import load_dotenv

load_dotenv()

host=os.get_env("HOST")
dbname=os.get_env("DBNAME")
user=os.get_env("USER")
password=os.get_env("PASS")
port=os.get_env("PORT")

def load_btc():
    transformed_data = transform_btc()
    
    # Define database connection
    conn = psycopg2.connect(
        host={host},
        dbname={dbname},
        user={user},
        password={password},
        port={port}
        )
    cur = conn.cursor()
    
    # Create tabke
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ticker(
            id SERIAL PRIMARY KEY,
            symbol TEXT,
            price_change FLOAT,
            price_change_percent FLOAT,
            weighted_avg_price FLOAT,      
            open_price FLOAT,
            high FLOAT,
            low FLOAT,
            closing_price FLOAT,
            volume FLOAT,
            quote_volume FLOAT,
            open_time TIMESTAMPTZ,
            close_time TIMESTAMPTZ,             
            first_id BIGINT,
            last_id BIGINT,
            count BIGINT
            );
        """
    )

    # Insert data
    for index, row in transformed_data.iterrows():
        cur.execute("""
            INSERT INTO ticker(
                symbol,
                price_change,
                price_change_percent,
                weighted_avg_price,      
                open_price,
                high,
                low,
                closing_price,
                volume,
                quote_volume,    
                open_time,
                close_time,             
                first_id,
                last_id,
                count
                )
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """, (row['symbol'], row['priceChange'], row['priceChangePercent'], row['weightedAvgPrice'],
          row['openPrice'], row['highPrice'], row['lowPrice'], row['lastPrice'], row['volume'],
       row['quoteVolume'], row['openTime'], row['closeTime'], row['firstId'], row['lastId'], row['count']
        ))
    
    # Commit changes to database
    conn.commit()

    # Display sample data to confirm load
    cur.execute("SELECT * FROM ticker ORDER BY close_time DESC LIMIT 1;")
    print("Data Loaded successfully:\n", cur.fetchone())

    # Close the connection
    cur.close()
    conn.close()
