from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

value_schema_str = """
{
    "type": "int"
}
"""

value_schema = avro.loads(value_schema_str)
value = 2

avroProducer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://0.0.0.0:8081'
}, default_value_schema=value_schema)

avroProducer.produce(topic='integer', value=value)
avroProducer.flush()
