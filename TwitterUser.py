import requests
import base64
import json
import sys
import datetime
import time
from colorama import Fore, Back, Style

value_schema = """{"name":"tweet","type": "string"}"""
#TODO: datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') per il ts

class TwitterUser:

    def __init__(self, name, surname):
        self.consumer_name = name # uso questo come consumer name
        # TODO: per ora do il surname come group_id, dopo:
        # - name: nickname dell'utente
        # - post a twitter che rende un id
        # - id come group id UNICO
        self.group = surname # uso questo come consumer group : deve essere unico altrimenti consuma messaggi di altri

    def get_username(self):
        return self.consumer_name

    def produce(self, topic, message_text):
        headers = {
        "Content-Type" : "application/vnd.kafka.json.v2+json",
        "Accept": "application/vnd.kafka.v2+json, application/vnd.kafka+json, application/json"
        }

        url = f"http://localhost:8082/topics/{topic}"

        message = {
          "value_schema": value_schema,
          "records": [
            {"key": self.consumer_name,
            "value": message_text
            }
          ]
        }

        r = requests.post(url, data=json.dumps(message), headers=headers)

    def get_consumer_instance(self):
        url=f"http://localhost:8082/consumers/{self.group}"

        headers = {
        "Content-Type" : "application/vnd.kafka.json.v2+json"
        }

        payload = {
          "name": f"{self.consumer_name}",
          "format": "binary",
          "auto.offset.reset": "earliest",
          "auto.commit.enable": "true" # se metto a 'true' cancella i messaggi: va messo per il singolo consumer
        }
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        print(r.text)

    def subscribe_to_topic(self,topic):
        url = f'http://localhost:8082/consumers/{self.group}/instances/{self.consumer_name}/subscription'
        headers = {
        "Content-Type" : "application/vnd.kafka.json.v2+json"
        }
        payload = {
          "topics": [
            f"{topic}"
          ]
        }
        r = requests.post(url, data=json.dumps(payload), headers = headers)

    def get_message(self):
        url = f'http://localhost:8082/consumers/{self.group}/instances/{self.consumer_name}/records?timeout=3000&max_bytes=300000'
        headers = {
        "Accept" : "application/vnd.kafka.binary.v2+json"
        }
        r = requests.get(url, headers=headers)
        json_data = json.loads(r.text)

        msg_list = []
        for i in range(len(json_data)):
            res = json_data[i]
            message = base64.b64decode(res["value"]).decode('utf-8')
            key = base64.b64decode(res["key"]).decode('utf-8')
            dict = {
                'topic': res["topic"],
                'key': key,
                'message': message
                }
            msg_list.append(dict)

        return msg_list


    def get_message_streaming(self):
        url = f'http://localhost:8082/consumers/{self.group}/instances/{self.consumer_name}/records?timeout=3000&max_bytes=300000'
        headers = {
        "Accept" : "application/vnd.kafka.binary.v2+json"
        }

        while True:
            time.sleep(1)
            r = requests.get(url, headers=headers)
            json_data = json.loads(r.text)
            for i in range(len(json_data)):
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
                res = json_data[i]
                message = base64.b64decode(res["value"]).decode('utf-8')
                key = base64.b64decode(res["key"]).decode('utf-8')
                if key != self.consumer_name:
                    print('\033[31;40m ======================================================= \033[0;37;40m')
                    print(f'\033[32;40m {self.consumer_name}, new tweet at time {st} \033[0;37;40m')
                    print('\033[31;40m ======================================================= \033[0;37;40m')
                    print(f'\033[33;40m User: \033[0;37;40m {key}')
                    print(f'\033[33;40m Tweet: \033[0;37;40m {message}')
                    print('\n')


    def delete_consumer_instance(self):
        url = f'http://localhost:8082/consumers/{self.group}/instances/{self.consumer_name}'
        headers = {
        "Content-Type" : "application/vnd.kafka.json.v2+json"
        }
        r = requests.delete(url, headers=headers)

#    def filter_homepage(self, filter):


if __name__ == '__main__':
    tu = TwitterUser('Matteo', 'Moreschini')
    tu.get_consumer_instance()
    tu.subscribe_to_topic('middleware')
    tu.get_message()
    tu.delete_consumer_instance()
