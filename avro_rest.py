import requests
import base64
import json
import sys
import base64
import avro

def subscribe_to_topic(topic):
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
    print(r.text)

def get_consumer_instance():
    group = 'my_test_group'
    consumer_name = 'my_name'
    url=f"http://localhost:8082/consumers/{group}"

    headers = {
    "Content-Type" : "application/vnd.kafka.json.v2+json"
    }

    payload = {
      "name": f"{consumer_name}",
      "format": "avro",
      "auto.offset.reset": "earliest",
      "auto.commit.enable": "true" # se metto a 'true' cancella i messaggi: va messo per il singolo consumer
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.text)
    return group, consumer_name

def get_message(group, name):
    url = f'http://localhost:8082/consumers/{group}/instances/{name}/records?timeout=3000&max_bytes=300000'
    headers = {
    "Accept" : "application/vnd.kafka.avro.v2+json"
    }
    r = requests.get(url, headers=headers)
    for m in r.json():
        print(m['value']['mentions'])


if __name__=='__main__':
    value_schema = open('tweet_schema.avsc', 'r', newline='').read()
    print(value_schema)
    topic = 'provaaaaaaa'
    producerurl=f"http://localhost:8082/topics/{topic}"

    headers = {
        "Content-Type":"application/vnd.kafka.avro.v2+json"
    }

    """
    payload = {
    'value_schema': value_schema,
    'records': [{
        'value':{"author":"Matteo", "content": "ciao"
        }
        }]
    }
    """
    payload = {
    'value_schema': value_schema,
    'records': [{
        'value':{"author":"Matteo", "content": "ciao",
        "timestamp":"now", "location":"Firenze", "tags":["ciao"], "mentions":["teomore"]
        }
        }]
    }
    r = requests.post(producerurl, data=json.dumps(payload), headers=headers)
    print(r.text)

    group, consumer_name = get_consumer_instance()
    subscribe_to_topic(f'{topic}')
    get_message(group, consumer_name)

    url = f'http://localhost:8082/consumers/{group}/instances/{consumer_name}'
    headers = {
    "Content-Type" : "application/vnd.kafka.json.v2+json"
    }
    r = requests.delete(url, headers=headers)
