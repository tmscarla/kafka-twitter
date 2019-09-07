from flask import Flask, request
app = Flask(__name__)

import requests
import time
import json
from TwitterUserAvro import TwitterUser
import threading

DEFAULT_TOPIC = 'streamingprova4'
START_TOPIC = 'start1'

@app.route('/tweet', methods=['POST'])
def produce_tweet():
    # fisse
    topic = START_TOPIC
    value_schema = open('tweet_schema.avsc', 'r', newline='').read()
    consumer_name = request.form['consumer_name']
    user_tweet_id = request.form['user_tweet_id']
    message_text = request.form['message_text']
    tags = [h for h in message_text.split() if h.startswith('#')]
    mentions = [h for h in message_text.split() if h.startswith('@')]

    headers = {
    "Content-Type" : "application/vnd.kafka.avro.v2+json",
    "Accept": "application/vnd.kafka.v2+json, application/vnd.kafka+json, application/json"
    }
    url = f"http://localhost:8082/topics/{topic}"
    message = {
    'value_schema': value_schema,
    'records': [{
        'value':{
            "author":f"{consumer_name}",
            "content": f"{message_text}",
            "timestamp":f"{time.time()}", # attach current timestamp
            "location":"Firenze",
            "tags": tags,
            "mentions": mentions,
            "id":  int(user_tweet_id)
        }
        }]
    }
    print(message)
    r = requests.post(url, data=json.dumps(message), headers=headers)
    return f'Response: {r.text}' # response to the publish request

@app.route('/users/id', methods=['POST'])
def subscribe():
    id = request.form['id']

    url=f"http://localhost:8082/consumers/{id}"

    headers = {
    "Content-Type" : "application/vnd.kafka.json.v2+json"
    }

    payload = {
      "name": f"{id}",
      "format": "avro",
      "auto.offset.reset": "earliest",
      "auto.commit.enable": "true" # se metto a 'true' cancella i messaggi: va messo per il singolo consumer
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f'{r.text}')
    json_data = json.loads(r.text)
    if 'error_code' in json_data:
        if json_data['error_code'] == 40902:
            print(f'Welcome back, {id}!')
        else:
            print('Error in creating your account...')
            # TODO: facci qualcosa
            # ad esempio uno while che finché non ritorna login cicla
    else:
        print(f"We're creating your KafkaTwitter account, {id}!")

    # subscribe to the topic
    url = f'http://localhost:8082/consumers/{id}/instances/{id}/subscription'
    headers = {
    "Content-Type" : "application/vnd.kafka.json.v2+json"
    }
    payload = {
      "topics": [
        f"{START_TOPIC}"
      ]
    }
    r = requests.post(url, data=json.dumps(payload), headers = headers)

    return f'Login done, {id}!s'

@app.route('/tweets/filter', methods=['POST'])
def streaming_filtering():
    filter = request.form['filter']

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
            query = "SELECT author,content,timestamp,location FROM test_kf_s_2"
            if city:
                query = query + f" WHERE location LIKE '{city}'"
            query = query +';'
            payload = { #"ksql": "SELECT * FROM prova_x; ",
                        "ksql": f'{query}',
                        "streamsProperties": {
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

@app.route('/tweets/cityfilter<cityfilter>mentionfilter<mentionfilter>tagfilter<tagfilter>/latest', methods=['GET'])
@app.route('/tweets/mentionfilter<mentionfilter>tagfilter<tagfilter>/latest', methods=['GET'])
@app.route('/tweets/cityfilter<cityfilter>mentionfilter<mentionfilter>/latest', methods=['GET'])
@app.route('/tweets/cityfilter<cityfilter>tagfilter<tagfilter>/latest', methods=['GET'])
@app.route('/tweets/cityfilter<cityfilter>/latest', methods=['GET'])
@app.route('/tweets/mentionfilter<mentionfilter>/latest', methods=['GET'])
@app.route('/tweets/tagfilter<tagfilter>/latest', methods=['GET'])
def batch_filtering(cityfilter=None, mentionfilter=None, tagfilter=None):

    return f"Il filtro città è {cityfilter}! Il filtro mention è {mentionfilter} Il filro tag è {tagfilter}"
