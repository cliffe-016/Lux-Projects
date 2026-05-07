import pandas as pd
import requests

def extract_btc():
    # Define base url and its parameters
    url = "http://data-api.binance.vision/api/v3/ticker"
    params = {
        'symbol': 'BTCUSDT',
        'windowSize': '7d'
    }
      
    # Send a GET request   
    raw = requests.get(url, params=params)

    # Store the response in json
    stg = raw.json()

    # Flatten the json response into a Dataframe
    data = pd.json_normalize(stg) # pd.Dataframe returned a ValueError, unless the arg was passed as a list
    
    return data

