from confluent_kafka import KafkaError, avro
from confluent_kafka.avro import AvroConsumer, AvroProducer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka import TopicPartition
from math import ceil

c = AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'join-ksql',
    'schema.registry.url': 'http://0.0.0.0:8081'
    })

c_partition0 = AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'join-ksql-specific',
    'schema.registry.url': 'http://0.0.0.0:8081'
    })

c_partition1 = AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'join-ksql-specific',
    'schema.registry.url': 'http://0.0.0.0:8081'
    })

c_partition2 = AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'join-ksql-specific',
    'schema.registry.url': 'http://0.0.0.0:8081'
    })

students_average =AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'students_average',
    'schema.registry.url': 'http://0.0.0.0:8081',
    'auto.offset.reset': 'earliest'
})

p0 = TopicPartition('students_result_source', 0)
p1 = TopicPartition('students_result_source', 1)
p2 = TopicPartition('students_result_source', 2)

# c.assign([Partition])

c.subscribe(['students_result_source'])
students_average.subscribe(['STUDENTS_AVERAGE'])
c_partition0.assign([p0])
c_partition1.assign([p1])
c_partition2.assign([p2])

searcher=[c_partition0, c_partition1, c_partition2]

key_schema_str = """
{
    "name": "average_key",
    "type": "int"
}
"""

value_schema_str = """
{
    "name": "average_value",
    "type": "record",
    "fields": [
        {"name": "student_id", "type": "int"},
        {"name": "name", "type": "string"},
        {"name": "average", "type": "int"}
    ]
}
"""

value_schema = avro.loads(value_schema_str)
key_schema = avro.loads(key_schema_str)

producer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://0.0.0.0:8081'
}, default_key_schema=key_schema, default_value_schema=value_schema)

    


while True:
    try:
        msg = c.poll(10)

    except SerializerError as e:
        print("Message deserialization failed for {}: {}".format(msg, e))
        break

    if msg is None:
        continue

    if msg.error():
        print("AvroConsumer error: {}".format(msg.error()))
        continue
    
    value = msg.value()
    key = msg.key()
    last_offset = int(msg.offset())
    partition = int(msg.partition())
    topic = msg.topic()
    print('')
    print('topic', topic)
    print('partition', partition)
    print('last_offset', last_offset, type(last_offset))
    print('key', key, type(key))
    print('value', value['NAME'], value['CATEGORY'], value['SCORE'])
    name = value['NAME']
    print('')
    print('{}\'s last three test (order by latest): '.format(value['NAME']))
    total = 0
    count = 0
    moving_offset = last_offset

    while count<3:
        if last_offset < 3:
            print('not enough data')
            break
        elif moving_offset == 0 and count<3:
            print('not enough data')
            break
        else:
            p = TopicPartition('students_result_source', partition, moving_offset)
            searcher[partition].seek(p)
            curr_msg = searcher[partition].poll(10)
            if curr_msg == None:
                continue
            elif int(curr_msg.key()) == key:
                count += 1
                value=curr_msg.value()
                print('no: ', value['ID'], ', category: ', value['CATEGORY'], ', score:', value['SCORE'])
                moving_offset -= 1
                total += value['SCORE']
            else:
                moving_offset -= 1

    if count < 3:
        print('the data is less than 3 record')
    else:
        average = int(ceil(total/3))
        print('average: ', average)
        data_average = {
            "student_id": key,
            "name": name,
            "average": average
        }
        data_key = key
        producer.produce(topic='average2', value=data_average, key=data_key)
        producer.flush()

c.close()
