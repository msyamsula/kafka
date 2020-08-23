from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka import TopicPartition


c = AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'messages-average',
    'schema.registry.url': 'http://0.0.0.0:8081',
    })

    
Partition = TopicPartition('ten-messages-average4', 0)
c.assign([Partition])
# c.seek(Partition)
# print(dir(c))
# # msg = c.poll(10)
# # print(msg.value(), msg.key(), msg.offset())


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
    
    data = msg.value()
    key = msg.key()
    last_offset = int(msg.offset())
    partition = msg.partition()
    topic = msg.topic()
    print('topic', topic)
    print('partition', partition)
    print('last_offset', last_offset, type(last_offset))
    print('key', key)
    print('value', data)
    print('')
    print('last ten messages:')
    total = 0

    for i in range(10):

        p = TopicPartition('ten-messages-average4', 0, last_offset-9+i)
        c.seek(p)
        curr_msg = c.poll(10)
        curr_data = curr_msg.value()
        curr_offset = curr_msg.offset()
        print(curr_data, curr_offset)

        total+=curr_data

    print('total last ten messages: ', total)
    print('average: ', total/10)


c.close()
