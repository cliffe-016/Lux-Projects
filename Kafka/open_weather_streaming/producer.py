import requests
from kafka import KafkaProducer 
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv('url')

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
topic = 'weather-info'

def extract():
    # Extract data from api 
    response = requests.get(url)

    # Convert to json
    results = response.json()
    return results

# Send data to kafka using a while loop
while True:
    results = extract()
    producer.send(topic, results)
    print(f"Sent: {results}")
    time.sleep(5)
