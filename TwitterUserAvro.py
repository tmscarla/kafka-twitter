import requests
import base64
import json
import sys
import datetime
import time
from colorama import Fore, Back, Style
import threading


class TwitterUser:

    def __init__(self, id):
        self.user_id = id # uso questo come consumer group : deve essere unico altrimenti consuma messaggi di altri
        self.value_schema = open('tweet_schema.avsc', 'r', newline='').read()
        # this is useful to track each tweet of a user
        self.user_tweet_id = 0
        # streaming
        self.streaming_messages = [] # this is userful to track the 5 minutes window of streaming messages
        self.streaming_thread = None

    def get_username(self):
        return self.user_id

    def get_user_tweet_id(self):
        return self.user_tweet_id

    def get_streaming_messages(self):
        time_interval = 10 # si mostrano solo i messaggi degli ultimi 5min=600s
        if len(self.streaming_messages)!=0:
            ts = time.time()
            self.streaming_messages = [x for x in self.streaming_messages if (ts-float(x[2]))<time_interval]

        return self.streaming_messages

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
                "author":f"{self.user_id}",
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
        url=f"http://localhost:8082/consumers/{self.user_id}"

        headers = {
        "Content-Type" : "application/vnd.kafka.json.v2+json"
        }

        payload = {
          "name": f"{self.user_id}",
          "format": "avro",
          "auto.offset.reset": "earliest",
          "auto.commit.enable": "true" # se metto a 'true' cancella i messaggi: va messo per il singolo consumer
        }
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        print(r.text)

    def subscribe_to_topic(self,topic):
        url = f'http://localhost:8082/consumers/{self.user_id}/instances/{self.user_id}/subscription'
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
        url = f'http://localhost:8082/consumers/{self.user_id}/instances/{self.user_id}/records?timeout=3000&max_bytes=300000'
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

    def start_streaming(self):
        self.streaming_thread = threading.Thread(target=self.get_message_streaming_ksql, args=())
        self.streaming_thread.daemon = True
        print(f'thread was running: {self.streaming_thread.isAlive()}')
        self.streaming_thread.start()
        print(f'now thread is running: {self.streaming_thread.isAlive()}')

    def stop_streaming(self):
        print(f'thread was running: {self.streaming_thread.isAlive()}')
        self.streaming_thread.join()
        time.sleep(0.2) # sleep per far sì che chiuda il processo
        print(f'now thread is running: {self.streaming_thread.isAlive()}')

    def get_message_streaming_ksql(self):
        s = requests.Session() # session creation

        def filtering(city = None):
            query = "SELECT author,content,timestamp,location FROM test_kf_s"
            if city:
                query = query + f" WHERE location LIKE '{city}'"
            query = query +';'
            payload = { #"ksql": "SELECT * FROM prova_x; ",
                        "ksql": f'{query}',
                        "streamsProperties": {
                            "ksql.streams.auto.offset.reset": "earliest"
                            }
                        }
            headers = {"Content-Type" : "application/vnd.ksql.v1+json; charset=utf-8"}
            req = requests.Request("POST","http://localhost:8088/query",
                                   headers=headers,
                                   data=json.dumps(payload)).prepare()

            resp = s.send(req, stream=True)

            for line in resp.iter_lines():
                if line:
                    yield(json.loads(line))

        def read_stream():
            self.streaming_messages = []
            for line in filtering('Firenze'):
                author = line['row']['columns'][0]
                content = line['row']['columns'][1]
                timestamp = line['row']['columns'][2]
                location = line['row']['columns'][3]
                self.streaming_messages.append([author,content,timestamp,location])
                print([author,content,timestamp,location])
        read_stream()

    def delete_consumer_instance(self):
        url = f'http://localhost:8082/consumers/{self.user_id}/instances/{self.user_id}'
        headers = {
        "Content-Type" : "application/vnd.kafka.json.v2+json"
        }
        r = requests.delete(url, headers=headers)


if __name__ == '__main__':
    tu = TwitterUser('Matteo', 'Moreschini')
    tu.get_consumer_instance()
    tu.subscribe_to_topic('mmmm')
    tu.produce('mmmm', 'try')
    tu.get_message()
    tu.delete_consumer_instance()
