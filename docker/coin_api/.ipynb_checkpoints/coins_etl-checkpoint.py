import requests
import pandas as pd
import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

def extract():
    # List required coins
    coins = ['bnb-bnb', 'btc-bitcoin', 'vrsc-verus', 'lunc-terra-classic', 'ada-cardano']

    # Loop through the coins to get data for each
    for coin_id in coins:
        url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}?quotes=USD"
        response = requests.get(url)

        # Only return data if connection succeeds
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"{response.status_code} error. Data Extraction failed.")

    return data

def transform():
    data = extract()
    
    # Normalize the data first
    df = pd.json_normalize(data)

    # Select required columns
    df = df[['name','symbol','last_updated','quotes.USD.price','quotes.USD.percent_change_24h']]

    # Rename columns
    df = df.rename(columns={ 
        'name':'coin_name', 'symbol':'coin_symbol',
        'quotes.USD.price': 'price',
        'quotes.USD.percent_change_24h': 'percent_change_24h'
        })

    return df.json()

def load():
    stg_df = transform()
    df = pd.DataFrame(stg_df)

    # Connect to db
    engine =create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    # Load data
    df.to_sql('coins_data', engine, if_exists='append', index=False)

    # Confirm data
    print(df.head())

if __name__ == "__main__":
    extract()
    transform()
    load()
