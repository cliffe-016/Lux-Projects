from extract import extract_btc
from transform import transform_btc
from load import load_btc

def main():
    print("Extracting data from binance api...")
    extract_btc()
    print("Data extracted successfully")

    print("Perfoming transformations...")
    transform_btc()
    print("Data transformed successfully")

    print("Loading data...")
    load_btc()


if __name__ == "__main__":
    main()
