import requests
import base64
import json
import sys
import datetime
import time
from colorama import Fore, Back, Style

class TwitterUser:

    def __init__(self, name, surname):
        self.consumer_name = name # uso questo come consumer name
        # TODO: per ora do il surname come group_id, dopo:
        # - name: nickname dell'utente
        # - post a twitter che rende un id
        # - id come group id UNICO
        self.group = surname # uso questo come consumer group : deve essere unico altrimenti consuma messaggi di altri
        self.value_schema = open('tweet_schema.avsc', 'r', newline='').read()
        # this is useful to track each tweet of a user
        self.user_tweet_id = 0

    def get_username(self):
        return self.consumer_name

    def produce(self, topic, message_text, tags=[], mentions=[]):
        headers = {
        "Content-Type" : "application/vnd.kafka.avro.v2+json",
        "Accept": "application/vnd.kafka.v2+json, application/vnd.kafka+json, application/json"
        }
        url = f"http://localhost:8082/topics/{topic}"
        message = {
        'value_schema': self.value_schema,
        'records': [{
            'value':{
                "author":f"{self.consumer_name}",
                "content": f"{message_text}",
                "timestamp":f"{time.time()}", # attach current timestamp
                "location":"Firenze",
                "tags": tags,
                "mentions": mentions,
                "id":  self.user_tweet_id
            }
            }]
        }
        print(message)
        r = requests.post(url, data=json.dumps(message), headers=headers)
        self.user_tweet_id += 1 # increment number of tweets of the user

    def get_consumer_instance(self):
        url=f"http://localhost:8082/consumers/{self.group}"

        headers = {
        "Content-Type" : "application/vnd.kafka.json.v2+json"
        }

        payload = {
          "name": f"{self.consumer_name}",
          "format": "avro",
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
        "Accept" : "application/vnd.kafka.avro.v2+json"
        }
        r = requests.get(url, headers=headers)
        print(r.text)
        msg_list = []
        for m in r.json():
            print(m)
            msg_list.append(m)

        return msg_list


    def get_message_streaming(self):
        url = f'http://localhost:8082/consumers/{self.group}/instances/{self.consumer_name}/records?timeout=3000&max_bytes=300000'
        headers = {
        "Accept" : "application/vnd.kafka.avro.v2+json"
        }

        while True:
            time.sleep(1)
            # must check the timestamp to show only last 5 min tweets
            current_ts = time.time()
            r = requests.get(url, headers=headers)
            msg_list = []
            for m in r.json():
                msg_ts = m['value']['timestamp']
                if (current_ts-float(msg_ts)) < 60:
                    print(m)
                    msg_list.append(m)

            return msg_list



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
    tu.subscribe_to_topic('mmmm')
    tu.produce('mmmm', 'try')
    tu.get_message()
    tu.delete_consumer_instance()
