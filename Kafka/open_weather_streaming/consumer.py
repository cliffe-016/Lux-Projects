from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'weather-info',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda d: json.loads(d.decode('utf-8'))
    )

print("Waiting for weather data...")
for message in consumer:
    print(f"Received: {message.value}")

