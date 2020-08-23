from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka import TopicPartition


class StringKeyAvroConsumer(AvroConsumer):

    def __init__(self, config):
        super(StringKeyAvroConsumer, self).__init__(config)

    def poll(self, timeout=None):
        """
        This is an overriden method from AvroConsumer class. This handles message
        deserialization using avro schema for the value only.

        @:param timeout
        @:return message object with deserialized key and value as dict objects
        """
        if timeout is None:
            timeout = -1
        message = super(AvroConsumer, self).poll(timeout)
        if message is None:
            return None
        if not message.value() and not message.key():
            return message
        if not message.error():
            if message.value() is not None:
                decoded_value = self._serializer.decode_message(message.value())
                message.set_value(decoded_value)
            # Don't try to decode the key
        return message

c = StringKeyAvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'anomaly',
    'schema.registry.url': 'http://localhost:8081',
    })

    
c.subscribe(['PENDING_COUNT'])


while True:
    try:
        msg = c.poll(1)

    except SerializerError as e:
        print("Message deserialization failed for {}: {}".format(msg, e))
        break

    if msg is None:
        continue

    if msg.error():
        print("AvroConsumer error: {}".format(msg.error()))
        continue
    
    dictionary = msg.value()
    data = dictionary['KSQL_COL_0']
    print(dictionary, data, type(data))

c.close()
