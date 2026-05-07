import pandas as pd
from extract import extract_weather

def transform_weather():
    # Define the df from the extract script and the json data as well for transformation
    data, stg_data = extract_weather()

    # To explicity flatten the nested weather column, use record_path
    data_weather = pd.json_normalize(stg_data, record_path=['weather']) # Pass stage the json data as list/dictionary is expected, not dataframe(TypeError would be returned)
    
    # Join the data 
    data = data.join(data_weather.add_prefix('weather_')) # The new columns are renamed by adding a prefix(weather_) to avoid the Value Error 

    # Drop the messy column
    transformed_data = data.drop(columns=['weather'])

    # Convert time columns from integer to timestamps
    time_columns = ['dt', 'sys.sunrise', 'sys.sunset']
    for col in time_columns:
        transformed_data[col] = pd.to_datetime(transformed_data[col], unit='s', utc=True)

    # Convert timezone column into a timezone
    transformed_data['timezone'] = pd.to_timedelta(transformed_data['timezone'], unit='s')
       

    return transformed_data
