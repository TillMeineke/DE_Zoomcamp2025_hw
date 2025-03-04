# Streaming module

## Menu
- docker
- docker-compose
- postgres
- Apache Flink

## Docker
- redpanda
- jobmanager (flink)
- taskmanager (flink)
- postgres

```bash
cd zoomcamp

docker-compose up
```

Make sure everything is running go in browser to `localhost:8081` for Flink Dashboard.

Setup connection in db-tool (pgaadmin4, dbbeaver, etc) to `localhost:5432` with user `postgres`, password `postgres`, database is `postgres`.

If jdbc connection is needed, use `jdbc:postgresql://localhost:5432/postgres`.

Query information schema to see tables:

```sql
SELECT * FROM information_schema.tables;
```

This is our landing zone for our data from Kafka.

Common pattern:  
Kafka -> read in RT -> dumped in db

Create `processed_events` table with db-tool:

```sql
CREATE TABLE processed_events (
    test_data INTEGER,
    event_timestamp TIMESTAMP
);
```

next: Add data to redpanda (simulates Kafka). use python script `producer.py`.

```python
producer = KafkaProducer(
    bootstrap_servers=[server], # server to connect to
    value_serializer=json_serializer # neede to serialize json
)
```

run script:

```bash
python3 src/producers/producer.py
```

We have a few jobs we will work with in `src/job`:
- `start_job.py` - start job
- `aggregation_job.py` - aggregation job

source - place where we read data from  
sink - place where we write data to

```python
def create_events_source_kafka(t_env):
    table_name = "events" # doesn't matter, only for flink
    pattern = "yyyy-MM-dd HH:mm:ss.SSS"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            test_data INTEGER,
            event_timestamp BIGINT,
            event_watermark AS TO_TIMESTAMP_LTZ(event_timestamp, 3),
            WATERMARK FOR event_watermark AS event_watermark - INTERVAL '15' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'test-topic', # from `producer.py`
            'properties.bootstrap.servers' = 'redpanda-1:29092',
            `scan.startup.mode` = 'earliest-offset', # read from beginning / other options: 'latest-offset' or timestamp
            `properties.auto.offset.reset` = 'earliest',
            'format' = 'json',
        );
        """
    t_env.execute_sql(source_ddl)
    return table_name
```

flink can connect to everything (RT integration tool with other APIs).