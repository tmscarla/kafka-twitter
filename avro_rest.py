import requests
import base64
import json
import sys
import base64
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
from confluent_kafka import avro

# TODO: usa questo schema avro
record_schema = avro.loads("""
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
""")

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
      "format": "avro",
      "auto.offset.reset": "earliest",
      "auto.commit.enable": "true" # se metto a 'true' cancella i messaggi: va messo per il singolo consumer
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
    json_data = json.loads(r.text)
    print(r.text)
    for i in range(len(json_data)):
        print('\033[31;40m ======================================================= \033[0;37;40m')
        print(f'\033[32;40m {consumer_name} Message {i+1} \033[0;37;40m')
        print('\033[31;40m ======================================================= \033[0;37;40m')
        res = json_data[i]
        #message = base64.b64decode(res["value"]).decode('utf-8')
        #key = base64.b64decode(res["key"]).decode('utf-8')
        print(f'\033[33;40m Topic: \033[0;37;40m {res["topic"]}')
        #print(f'\033[33;40m Key: \033[0;37;40m {key}')
        print(f'\033[33;40m Message: \033[0;37;40m {message}')
        print('\n')

def delete_consumer_instance(group, consumer_name):
    # PER ELIMINARE
    url = f'http://localhost:8082/consumers/{group}/instances/{consumer_name}'
    headers = {
    "Content-Type" : "application/vnd.kafka.json.v2+json"
    }
    r = requests.delete(url, headers=headers)

if __name__=='__main__':
    value_schema = """{"name":"tweet","type": "string"}"""
    message = {
      "value_schema": value_schema,
      "records": [
        {"key": 'Tommaso',
        "value": 'Alessio sei un coglione!'
        }, {"key": 'Matteo',
        "value": 'Chi cazzo è Alessio?'
        }, {"key": 'Tommaso',
        "value": 'Boh uno che fa Middleware con noi'
        }
      ]

    }

    avro_schema = {
        "namespace": "confluent.io.examples.serialization.avro",
        "name": "User",
        "type": "record",
        "fields": [
            {"name": "name", "type": "string"}
        ]
    }

    msg = {
    "value_schema": avro_schema,
    "records":[
    {"value": "test_user"}
    ]
    }

    # 1) First, let's produce a message
    topic = 'middleware'
    produce(msg, topic)
    # 2) Let's create a consumer instance
    """
    group = 'Russo Introito'
    consumer = 'Alessio' # questo sarà poi l'utente, gli assegnerò un nome utente unico & un ID
    get_consumer_instance(group, consumer)
    # 3) Subscribe consumer to a topic
    subscribe_to_topic(topic, group, consumer)
    # 4) Now let's get the messages produced on the subscribed topics
    get_message(group, consumer)
    # 5) Finally, delete the consumer instance
    delete_consumer_instance(group, consumer)
    """
