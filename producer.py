from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': "localhost:9092",
        'client.id': socket.gethostname(),
        'default.topic.config': {'acks': 'all'}}

producer = Producer(conf)

value1 = {'wikwik': 'enak'}
value2 = 'wikwik'
value3 = [1,2,3,4]
value4 = 4

producer.produce('duality', 'message from duality topics')
# producer.produce('users', value2, 'the_key')


# for i in range(10):
#     producer.produce('baru', {'wikwik': 'enak'})
#     producer.produce('test', str(i), str(i) )
# producer.produce('baru', '1', 'test')
producer.flush()