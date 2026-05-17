# Catchy Title
Standard practise for ETL/ELT pipelines is to orchestrate batch extractions with Airflow, Dagster or a similar tool with dbt transformations to gather daily data from an API. However, what would happen if the data wasn't collected but rather is being collected in the moment. Scheduled batch scripts are unable to keep up when you go from analyzing yesterday's data to needing real-time metrics now. This is where streaming comes in. You would require a system designed for continuous event streaming. This is where Apache Kafka comes in.
Kafka is an open-source distributed event streaming platform.
It acts as a massive central nervous system, allowing data to flow continuously from source to destination.
To understand how Kafka works, I'll break down its core concepts using a live streaming project: 
[a pipeline that extracts real-time weather data from the OpenWeatherMap API and streams it directly into a Cassandra database.](https://github.com/Cliffe16/Lux_Assignments/tree/main/Kafka/open_weather_streaming)

## Topic
Whearas in a database, you insert data into a **table**, in Kafka, you push data to a **topic.** In the weather pipeline, the topic is simply as:
```Python
topic = 'weather_info'
```
Every API response pulled for Nairobi's current weather conditions will be published to this specific topic.
```Python
producer.send(topic, {api_response})
```

## Producer
A producer is any application that publishes data to a Kafka topic. Their only job is to gather data and push it to the broker. For this project, `producer.py` acts as the producer, it requests data from the weather api, receives a json payload, and sends it to the topic every 5 seconds.

```Python
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

while True:
    results = extract()
    producer.send(topic, results)
    time.sleep(5)
```

### Serialization
Kafka being a streaming platform, it does not understand complex dataframes due to its fast data delivery nature. To send the weather data, the json response is first converted into a **byte** array hence the `value_serializer` argument in the code block above. Conversely, when the data reaches its destination, it must be deserialized back into a readable format. This is why the consumer script includes a matching deserializer `value_deserializer`.

## Consumer
A consumer subscribes to one or more topics, reads the stream of incoming records and processes them. In `consumer.py`, the script acts as a continuous listener on the `weather-info` topic. As soon as a new weather event arrives, the consumer receives the event, flattens the nested JSON, converts Unix timestamps into standard datetime formats and executes an `INSERT` statement to load the clean data into a Cassandra database table.
```Python
for message in consumer:
    raw_data = message.value
    
    # ... data flattening and timestamp conversion ...

    session.execute(insert_query, (
        raw_data.get('id'),
        unix_to_dt(sys_data.get('sunrise')),
        # ... other fields ...
        sys_data.get('country')
    ))
```
Unlike a standard Python `for loop` that ends when it reaches the bottom of a list, a Kafka `for message in consumer` loop is infinite. 

**_Why use Kafka?_**
Because, if the OpenWeatherMap API suddenly surges, sending thousands of records per second and you have a Python script writing directly to Cassandra, the database might become overwhelmed, lock up and crash, taking your entire pipeline down with it. Kafka acts as an indestructible shock absorber. The Producer can dump millions of records into the Kafka topic at lightning speed and Kafka simply holds onto them. The Consumer will then read from the topic at its own pace,processing and inserting records into Cassandra as fast as it can without overwhelming the database. Even if the consumer crashes, Kafka remembers exactly where it left off, ensuring zero data loss when it restarts.

