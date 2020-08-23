from kafka import KafkaConsumer

c = KafkaConsumer(
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    group_id='kafka-python',
    key_deserializer='org.apache.kafka.common.serialization.StringDeserializer')

c.subscribe(topics='students_source9')

for messages in c:
    print('message')

c.close()