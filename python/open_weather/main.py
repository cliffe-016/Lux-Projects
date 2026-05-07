from extract import extract_weather
from transform import transform_weather
from load import load_weather
def main():
    data = extract_weather()
    transformed_data = transform_weather()

    print("Extracting data...")
    extract_weather()
    print("Data Extracted successfully:\n", data)
    print("--------------------------------------")
    
    print("Transforming data")
    transform_weather()
    print("Data transformed successfully\n", transformed_data)

    print("Loading Data")
    load_weather()

if __name__ == "__main__":
    main()
