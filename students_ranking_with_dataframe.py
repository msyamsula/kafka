from confluent_kafka import KafkaError, avro
from confluent_kafka.avro import AvroConsumer, AvroProducer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka import TopicPartition
from math import ceil
from calculation import calculate_average, calculate_ranking
from schema import key_schema_avg_str, key_schema_rank_str, value_schema_avg_str, value_schema_rank_str
import datetime

c = AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'join-ksql',
    'schema.registry.url': 'http://0.0.0.0:8081'
    })

# c.assign([Partition])

c.subscribe(['students_result_source'])

value_schema_avg = avro.loads(value_schema_avg_str)
key_schema_avg = avro.loads(key_schema_avg_str)
value_schema_rank = avro.loads(value_schema_rank_str)
key_schema_rank = avro.loads(key_schema_rank_str)

producer_avg = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://0.0.0.0:8081'
}, default_key_schema=key_schema_avg, default_value_schema=value_schema_avg)

producer_rank = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://0.0.0.0:8081'
}, default_key_schema=key_schema_rank, default_value_schema=value_schema_rank)

while True:
    start = datetime.datetime.now()
    print(start)
    try:
        msg = c.poll()

    except SerializerError as e:
        print("Message deserialization failed for {}: {}".format(msg, e))
        break

    if msg is None:
        continue

    if msg.error():
        print("AvroConsumer error: {}".format(msg.error()))
        continue
    
    value = msg.value()
    key = int(msg.key())
    print('value', value['NAME'], value['CATEGORY'], value['SCORE'])
    name = value['NAME']
    average = calculate_average(name)

    if average == -3:
        continue

    print('average', average)
    data_average = {
        "student_id": key,
        "name": name,
        "average": average
    }
    producer_avg.produce(topic='average2', value=data_average, key=key)
    producer_avg.flush()

    students_rank = calculate_ranking()
    rank=''
    for student in students_rank:
        producer_rank.produce(topic='students_rank', value=student, key=student['ranking'])
        producer_rank.flush()
        if student['name'] == name:
            rank = student['ranking']

    print('current rank: ', rank)
    end=datetime.datetime.now()
    print(end)
    print(end-start)
c.close()
