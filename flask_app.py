from flask import Flask, request
app = Flask(__name__)
import requests
import time
import json
from TwitterUserAvro import TwitterUser

DEFAULT_TOPIC = 'test_kf_s'

@app.route('/tweet', methods=['POST'])
def produce_tweet():
    # fisse
    topic = DEFAULT_TOPIC
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
        f"{DEFAULT_TOPIC}"
      ]
    }
    r = requests.post(url, data=json.dumps(payload), headers = headers)

    return f'Login done, {id}!s'
