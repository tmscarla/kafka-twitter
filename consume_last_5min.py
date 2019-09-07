from datetime import datetime
from confluent_kafka.avro import AvroConsumer
from confluent_kafka import TopicPartition
import time

topic  = "start1"
broker = "localhost:9092"

# lets check messages of the first day in New Year
current_ts = time.time()
date_in  = current_ts - 60
date_out = current_ts

consumer = AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'groupid',
    'schema.registry.url': 'http://127.0.0.1:8081'})

consumer.poll(10)  # we need to read message or call dumb poll before seeking the right position

tp = TopicPartition(topic, 0) # partition n. 0

# in fact you asked about how to use 2 methods: offsets_for_times() and seek()
rec_in  = consumer.offsets_for_times([tp], 60)
rec_out = consumer.offsets_for_times([tp], 30)
print(rec_in)
print(rec_out)
#consumer.seek(tp, rec_in[tp].offset) # lets go to the first message in New Year!
"""
c = 0
for msg in consumer:
  if msg.offset >= rec_out[tp].offset:
    break

  c += 1
  # message also has .timestamp field

print("{c} messages between {_in} and {_out}".format(c=c, _in=str(date_in), _out=str(date_out)))
"""
