import requests
import base64
import json
import sys

# TODO: usa questo schema avro
avro_schema = """
    {
        "namespace": "confluent.io.examples.serialization.avro",
        "name": "User",
        "type": "record",
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "favorite_number", "type": "int"},
            {"name": "favorite_color", "type": "string"}
        ]
    }
"""

def produce(message, topic):
    headers = {
    "Content-Type" : "application/vnd.kafka.json.v2+json",
    "Accept": "application/vnd.kafka.v2+json, application/vnd.kafka+json, application/json"
    }

    url = f"http://localhost:8082/topics/{topic}"

    r = requests.post(url, data=json.dumps(message), headers=headers)
    print(r.text)

def get_consumer_instance(group, consumer_name):
    url=f"http://localhost:8082/consumers/{group}"

    headers = {
    "Content-Type" : "application/vnd.kafka.json.v2+json"
    }

    payload = {
      "name": f"{consumer_name}",
      "format": "binary",
      "auto.offset.reset": "earliest",
      "auto.commit.enable": "false"
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.text)


def subscribe_to_topic(topic, group, consumer_name): # group e consumer name li prenderà poi da sé, sarà uno dei metodi di un utente
    url = f'http://localhost:8082/consumers/{group}/instances/{consumer_name}/subscription'
    headers = {
    "Content-Type" : "application/vnd.kafka.json.v2+json"
    }
    payload = {
      "topics": [
        f"{topic}"
      ]
    }
    r = requests.post(url, data=json.dumps(payload), headers = headers)

def get_message(group,consumer_name):
    url = f'http://localhost:8082/consumers/{group}/instances/{consumer_name}/records?timeout=3000&max_bytes=300000'
    headers = {
    "Accept" : "application/vnd.kafka.binary.v2+json"
    }
    r = requests.get(url, headers=headers)
    print(r.text)

def delete_consumer_instance(group, consumer_name):
    # PER ELIMINARE
    url = f'http://localhost:8082/consumers/{group}/instances/{consumer_name}'
    headers = {
    "Content-Type" : "application/vnd.kafka.json.v2+json"
    }
    r = requests.delete(url, headers=headers)

if __name__=='__main__':
    value_schema = """{"name":"int","type": "int"}"""
    message = {
      "value_schema": value_schema,
      "records": [
        {
        "value": 15
        }
      ]
    }

    # 1) First, let's produce a message
    topic = 'avrotest'
    produce(message, topic)
    # 2) Let's create a consumer instance
    group = 'test_group'
    consumer = 'Matteo' # questo sarà poi l'utente, gli assegnerò un nome utente unico & un ID
    get_consumer_instance(group, consumer)
    # 3) Subscribe consumer to a topic
    subscribe_to_topic(topic, group, consumer)
    # 4) Now let's get the messages produced on the subscribed topics
    get_message(group, consumer)
    # 5) Finally, delete the consumer instance
    delete_consumer_instance(group, consumer)
