import pandas as pd
from extract import extract_btc 

def transform_btc():
    data = extract_btc()
    
    # Convert time columns from integers to utc timestamps
    time_columns = ['openTime', 'closeTime']

    for col in time_columns:
        data[col] = pd.to_datetime(data[col], unit = 'ms', utc=True)

    transformed_data = data
    
    return transformed_data
