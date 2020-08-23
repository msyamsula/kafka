from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

value_schema_str = """
{
   "namespace": "my.test",
   "type": "string",
   "name": "testing"
}
"""

value_schema = avro.loads(value_schema_str)
value = 'wow'

avroProducer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://0.0.0.0:8081'
}, default_value_schema=value_schema)

avroProducer.produce(topic='connect-test', value=value)
avroProducer.flush()
