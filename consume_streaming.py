"""
from confluent_kafka import Consumer, KafkaError

# Set 'auto.offset.reset': 'smallest' if you want to consume all messages
# from the beginning of the topic the first time that this runs.
#
# If you want to monitor your data streams through Confluent Control Center,
# make sure you've installed the interceptors and then uncomment
# the 'plugin.library.paths' config line
# Ref: https://docs.confluent.io/current/control-center/docs/installation/clients.html#installing-control-center-interceptors
settings = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'lu',
#    'plugin.library.paths': 'monitoring-interceptor',
    'default.topic.config': {'auto.offset.reset': 'largest'}
}
c = Consumer(settings)

c.subscribe(['start1'])


while True:
    msg = c.poll()

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()
"""
from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka import TopicPartition
import time
import datetime
import json

c = AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'groupid',
    'schema.registry.url': 'http://127.0.0.1:8081'})

#c.subscribe(['start1'])
c.assign([TopicPartition("start6", 0,0)])

print(f"Assignements: {c.assignment()}")
topic_partition = TopicPartition("start6", partition=0)
low, high = c.get_watermark_offsets(topic_partition)
print(f"the latest offset is {high}, the low is {low}")
print(f"consumer position: {c.position([topic_partition])}")

WINDOW_LEN = 2 # calcolo high offset - WINDOW_LEN

topic_partition2 = TopicPartition("start6", 0, high-WINDOW_LEN)
c.seek(topic_partition2)
low, high = c.get_watermark_offsets(topic_partition)
print(f"the latest offset is {high}, the low is {low}")
print(f"consumer position: {c.position([topic_partition])}")

pos = c.position([topic_partition])
while pos[0].offset<high:
    try:
        msg = c.poll(0)

    except SerializerError as e:
        print("Message deserialization failed for {}: {}".format(msg, e))
        break

    if msg is None:
        continue

    if msg.error():
        print("AvroConsumer error: {}".format(msg.error()))
        continue

    author = msg.value()['author']
    content = msg.value()['content']
    timestamp = datetime.datetime.fromtimestamp(float(msg.timestamp()[1]/1000)).strftime('%H:%M:%S, %d-%m-%Y')
    location = msg.value()['location']
    tags = [h for h in content.split() if h.startswith('#')]
    mentions = [h for h in content.split() if h.startswith('@')]
    print(f"[{author}] {content} ({location} - {timestamp})")
    pos = c.position([topic_partition])
c.close()
