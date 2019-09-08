from flask import Flask, request, Response
app = Flask(__name__)

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import requests
import time
import json
from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka import TopicPartition
import time
import datetime
from flask import stream_with_context, request, Response

# defaults
TOPIC = 'start6'
BOOTSTRAP_SERVERS = 'localhost:9092'#'10.0.0.6:9092, 10.0.0.4:9092'
SCHEMA_REGISTRY_URL = 'http://127.0.0.1:8081'
KEY_SCHEMA = avro.loads(open('key_schema.avsc', 'r', newline='').read())
VALUE_SCHEMA = avro.loads(open('tweet_schema_3.avsc', 'r', newline='').read())
WINDOW_LEN = 10

# Subscription URL
@app.route('/users/id', methods=['POST'])
def subscribe():
    id = request.form['id']
    # create consumer and producer
    c = AvroConsumer(
        {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'group.id': f'{id}',
        'schema.registry.url': SCHEMA_REGISTRY_URL
        }
    )
    # assign the partition
    c.assign([TopicPartition(TOPIC, 0,0)])
    print(f"Assignments: {c.assignment()}")

    return f"Logged in as {id}"

# Publish URL
@app.route('/tweet', methods=['POST'])
def produce_tweet():
    # TODO: metti EOS

    id = request.form['id']
    content = request.form['content']
    location = request.form['location']
    # extract tags and mentions :)
    tags = [h for h in content.split() if h.startswith('#')]
    mentions = [h for h in content.split() if h.startswith('@')]

    value = {
        "author": f"{id}",
        "content": f"{content}",
        "location": f"{location}",
        "tags": tags,
        "mentions": mentions
    }
    key = {"name": f"{id}"}

    p = AvroProducer({
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'broker.address.family': 'v4',
        'schema.registry.url': SCHEMA_REGISTRY_URL
        }, default_key_schema=KEY_SCHEMA, default_value_schema=VALUE_SCHEMA)

    p.produce(topic=TOPIC, value=value, key=key)
    p.flush()
    return 'Tweet published!'


# Batch (with filtering) URL
@app.route('/tweets/cityfilter=<cityfilter>&mentionfilter=<mentionfilter>&tagfilter=<tagfilter>/latest', methods=['GET'])
@app.route('/tweets/mentionfilter=<mentionfilter>&tagfilter=<tagfilter>/latest', methods=['GET'])
@app.route('/tweets/cityfilter=<cityfilter>&mentionfilter=<mentionfilter>/latest', methods=['GET'])
@app.route('/tweets/cityfilter=<cityfilter>&tagfilter=<tagfilter>/latest', methods=['GET'])
@app.route('/tweets/cityfilter=<cityfilter>/latest', methods=['GET'])
@app.route('/tweets/mentionfilter=<mentionfilter>/latest', methods=['GET'])
@app.route('/tweets/tagfilter=<tagfilter>/latest', methods=['GET'])
@app.route('/tweets/nofilters/latest', methods=['GET'])
def batch_filtering(cityfilter=None, mentionfilter=None, tagfilter=None):
    # TODO: metti auto.commit = True? oppure tracka l'ultimo offset

    if 'username' in request.cookies:
        username = request.cookies['username']
        print(f"Ok, {username}, let's fetch the latest tweets!")
        c = AvroConsumer(
            {
            'bootstrap.servers': BOOTSTRAP_SERVERS,
            'group.id': username,
            'schema.registry.url': SCHEMA_REGISTRY_URL
            }
        )
        c.assign([TopicPartition(TOPIC, 0,0)])
        low_offset, high_offset = c.get_watermark_offsets(TopicPartition(TOPIC, 0))
        print(f"the latest offset is {high_offset}, the low is {low_offset}")
        print(f"consumer position: {c.position([TopicPartition(TOPIC, 0)])}")

        # move consumer to offset=high_offset-WINDOW_LEN (only if > 0)
        if high_offset-WINDOW_LEN>0:
            new_offset = high_offset-WINDOW_LEN
        else:
            new_offset = low_offset
        c.seek(TopicPartition(TOPIC, 0, new_offset))

        msgs = [] # to store the messages to be returned
        pos = c.position([TopicPartition(TOPIC, 0, new_offset)])
        while pos[0].offset<high_offset:
            try:
                msg = c.poll(0)

            except SerializerError as e:
                print("Message deserialization failed for {}: {}".format(msg, e))
                break

            if msg is None:
                continue

            if msg.error():
                print("AvroConsumer error: {}".format(msg.error()))
                continue

            author = msg.value()['author']
            content = msg.value()['content']
            timestamp = datetime.datetime.fromtimestamp(float(msg.timestamp()[1]/1000)).strftime('%H:%M:%S, %d-%m-%Y')
            location = msg.value()['location']
            tags = [h[1:] for h in content.split() if h.startswith('#')]
            mentions = [h[1:] for h in content.split() if h.startswith('@')]
            print(f"[{author}] {content} ({location} - {timestamp}) mentions: {mentions}")
            print(f"consumer position: {c.position([TopicPartition(TOPIC, 0, new_offset)])}")
            pos = c.position([TopicPartition(TOPIC, 0, new_offset)])

            if cityfilter!=None and mentionfilter!=None and tagfilter!=None:
                if (location == cityfilter) and (mentionfilter in mentions) and (tagfilter in tags):
                    msgs.append(f"[{author}] {content} ({location} - {timestamp})")
            elif cityfilter==None and mentionfilter!=None and tagfilter!=None:
                if (mentionfilter in mentions) and (tagfilter in tags):
                    msgs.append(f"[{author}] {content} ({location} - {timestamp})")
            elif cityfilter!=None and mentionfilter==None and tagfilter!=None:
                if (location == cityfilter) and (tagfilter in tags):
                    msgs.append(f"[{author}] {content} ({location} - {timestamp})")
            elif cityfilter!=None and mentionfilter!=None and tagfilter==None:
                if (location == cityfilter) and (mentionfilter in mentions):
                    msgs.append(f"[{author}] {content} ({location} - {timestamp})")
            elif cityfilter!=None and mentionfilter==None and tagfilter==None:
                if (location == cityfilter):
                    msgs.append(f"[{author}] {content} ({location} - {timestamp})")
            elif cityfilter==None and mentionfilter!=None and tagfilter==None:
                if (mentionfilter in mentions):
                    msgs.append(f"[{author}] {content} ({location} - {timestamp})")
            elif cityfilter==None and mentionfilter==None and tagfilter!=None:
                if (tagfilter in tags):
                    msgs.append(f"[{author}] {content} ({location} - {timestamp})")
            else:
                msgs.append(f"[{author}] {content} ({location} - {timestamp})")
            l = c.offsets_for_times([TopicPartition(TOPIC, 0)], 10)
            print(f"Offset for times: {l}")
        c.close()
        # finally return dictonary of messages
        return {"results": msgs}
    else:
        return {"results": ['Oooops, your are not logged in...']}

# Streaming (with filters) URL
@app.route('/tweets/cityfilter=<cityfilter>&mentionfilter=<mentionfilter>&tagfilter=<tagfilter>', methods=['POST'])
@app.route('/tweets/mentionfilter=<mentionfilter>&tagfilter=<tagfilter>', methods=['POST'])
@app.route('/tweets/cityfilter=<cityfilter>&mentionfilter=<mentionfilter>', methods=['POST'])
@app.route('/tweets/cityfilter=<cityfilter>&tagfilter=<tagfilter>', methods=['POST'])
@app.route('/tweets/cityfilter=<cityfilter>', methods=['POST'])
@app.route('/tweets/mentionfilter=<mentionfilter>', methods=['POST'])
@app.route('/tweets/tagfilter=<tagfilter>', methods=['POST'])
@app.route('/tweets/nofilters', methods=['GET'])
def streaming_filtering(cityfilter=None, mentionfilter=None, tagfilter=None):
    if 'username' in request.cookies:
        # TODO ... chunked
        username = request.cookies['username']
        print(f"Ok, {username}, let's stream the latest tweets!")
        c = AvroConsumer(
            {
            'bootstrap.servers': BOOTSTRAP_SERVERS,
            'group.id': username,
            'schema.registry.url': SCHEMA_REGISTRY_URL
            }
        )
        c.assign([TopicPartition(TOPIC, 0,0)])
        low_offset, high_offset = c.get_watermark_offsets(TopicPartition(TOPIC, 0))
        print(f"the latest offset is {high_offset}, the low is {low_offset}")
        print(f"consumer position: {c.position([TopicPartition(TOPIC, 0)])}")

        # move consumer to top
        c.seek(TopicPartition(TOPIC, 0, high_offset))

        msgs = []
        pos = c.position([TopicPartition(TOPIC, 0, high_offset)])
        def gen(msgs): # generator funciton for streaming
            print('ciao')
            while True:
                try:
                    msg = c.poll(1)

                except SerializerError as e:
                    print("Message deserialization failed for {}: {}".format(msg, e))
                    break

                if msg is None:
                    current_ts = time.time()
                    msgs = [m for m in msgs if (float(current_ts)-float(m[1]))<10]
                    ret_msgs = [m[0] for m in msgs]
                    yield f' `{json.dumps(ret_msgs)}` '
                    continue

                if msg.error():
                    current_ts = time.time()
                    msgs = [m for m in msgs if (float(current_ts)-float(m[1]))<10]
                    ret_msgs = [m[0] for m in msgs]
                    yield f' `{json.dumps(ret_msgs)}` '
                    print("AvroConsumer error: {}".format(msg.error()))
                    continue

                print('booh')
                # get message fields
                author = msg.value()['author']
                content = msg.value()['content']
                timestamp = datetime.datetime.fromtimestamp(float(msg.timestamp()[1]/1000)).strftime('%H:%M:%S, %d-%m-%Y')
                location = msg.value()['location']
                tags = [h[1:] for h in content.split() if h.startswith('#')]
                mentions = [h[1:] for h in content.split() if h.startswith('@')]
                # create display_message
                display_message = f"[{author}] {content} ({location} - {timestamp}) mentions: {mentions}"
                display_message = display_message.replace("`", "'") # serve per leggere lo streaming
                message_ts = float(msg.timestamp()[1]/1000)
                print(f"{display_message}")
                print(f"consumer position: {c.position([TopicPartition(TOPIC, 0, high_offset)])}")
                pos = c.position([TopicPartition(TOPIC, 0, high_offset)])

                if cityfilter!=None and mentionfilter!=None and tagfilter!=None:
                    if (location == cityfilter) and (mentionfilter in mentions) and (tagfilter in tags):
                        msgs.append((display_message,message_ts))
                elif cityfilter==None and mentionfilter!=None and tagfilter!=None:
                    if (mentionfilter in mentions) and (tagfilter in tags):
                        msgs.append((display_message,message_ts))
                elif cityfilter!=None and mentionfilter==None and tagfilter!=None:
                    if (location == cityfilter) and (tagfilter in tags):
                        msgs.append((display_message,message_ts))
                elif cityfilter!=None and mentionfilter!=None and tagfilter==None:
                    if (location == cityfilter) and (mentionfilter in mentions):
                        msgs.append((display_message,message_ts))
                elif cityfilter!=None and mentionfilter==None and tagfilter==None:
                    if (location == cityfilter):
                        msgs.append((display_message,message_ts))
                elif cityfilter==None and mentionfilter!=None and tagfilter==None:
                    if (mentionfilter in mentions):
                        msgs.append((display_message,message_ts))
                elif cityfilter==None and mentionfilter==None and tagfilter!=None:
                    if (tagfilter in tags):
                        msgs.append((display_message,message_ts))
                else:
                    msgs.append((display_message,message_ts))

                # remove old messages
                current_ts = time.time()
                msgs = [m for m in msgs if (float(current_ts)-float(m[1]))<10]
                ret_msgs = [m[0] for m in msgs]
                yield f' `{json.dumps(ret_msgs)}` '

        return Response(stream_with_context(gen(msgs)))
    else:
        return {"results": ['Oooops, your are not logged in...']}

@app.route('/time', methods=['GET'])
def streamed_response():
    msg = []
    def generate(msg):
        count = 0
        window = 5
        while True:
            count +=1
            message = str(count)
            message = message.replace("`", "'")
            msg.append(message)
            time.sleep(2)
            #for i in msg:
            #    print(i)
            #    yield json.dumps(f"`{i}`")
            msg = [x for x in msg if int(x)>len(msg)-window]
            print(json.dumps(msg))
            yield f' `{json.dumps(msg)}` '
    return Response(stream_with_context(generate(msg)))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000')
