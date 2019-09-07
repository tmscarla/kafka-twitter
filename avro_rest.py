from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import geocoder
import reverse_geocoder as rg
import pprint
import requests
import json

def reverseGeocode():
    g = geocoder.ip('me')
    print(g.latlng)
    # Coorinates tuple.Can contain more than one pair.
    coordinates =(g.latlng[0], g.latlng[1])
    result = rg.search(coordinates)
    # result is a list containing ordered dictionary.
    print(f"{result[0]['name']}, {result[0]['cc']}")
    return f"{result[0]['name']}, {result[0]['cc']}"

key_schema_str = """
{
   "namespace": "model.username",
   "name": "key",
   "type": "record",
   "fields" : [
     {
       "name" : "name",
       "type" : "string"
     }
   ]
}
"""

value_schema = avro.loads(open('tweet_schema_3.avsc', 'r', newline='').read())
key_schema = avro.loads(key_schema_str)
username = 'Teo'
content = 'yoyo #come @ciao'
location = reverseGeocode()
tags = [h for h in content.split() if h.startswith('#')]
mentions = [h for h in content.split() if h.startswith('@')]

TOPIC = 'start4'

value = {
    "author": f"{username}",
    "content": f"{content}",
    "location": f"{location}",
    "tags": tags,
    "mentions": mentions
}
key = {"name": f"{username}"}


avroProducer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://127.0.0.1:8081'
    }, default_key_schema=key_schema, default_value_schema=value_schema)

avroProducer.produce(topic='start4', value=value, key=key)
avroProducer.flush()
