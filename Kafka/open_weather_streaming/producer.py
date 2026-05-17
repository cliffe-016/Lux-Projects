import requests
from kafka import KafkaProducer 
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
topic = 'weather-info'

def extract():
    # Extract data from api 
    url="https://api.openweathermap.org/data/2.5/weather?lat=-1.2921&lon=36.8219&appid=c84569ede6e5f4688e4e8fc032ab4e6f"
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
