import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Define api endpoint
url = os.getenv("url")

def extract_weather():
    # Access the API and check response
    raw_data = requests.get(url)

    # Convert data to json
    stg_data = raw_data.json()

    # Flatten JSON data into a dataframe
    # The data returned containes mixed series i.e dictionaries and lists
    data = pd.json_normalize(stg_data)

    return data, stg_data # Both are required for transformation
    
