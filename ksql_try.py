import requests
import json

# <path-to-confluent>/bin/confluent local start
# urls
base_url = "http://0.0.0.0:8088/ksql"
query_url = "http://localhost:8088/query"

input_topic = 'test_kt'
output_topic = 'test_kf_s'

# create ksql stream
create_stream = False
if create_stream:
    headers = {
        "Content-Type" : "application/vnd.ksql.v1+json",
        "Accept" : "application/vnd.ksql.v1+json"
    }

    payload = {
        "ksql": f"CREATE STREAM {output_topic} WITH (KAFKA_TOPIC='{input_topic}',VALUE_FORMAT='AVRO');",
        "streamsProperties": {
          "ksql.streams.auto.offset.reset": "earliest"
        }

    }

    r = requests.post(base_url, data=json.dumps(payload), headers=headers)
    print(r.text)

# read ksql
do_streaming = False

if do_streaming:
    s = requests.Session() # session creation

    def filtering(city = None):
        query = f"SELECT * FROM {output_topic}"
        if city:
            query = query + f" WHERE location LIKE '{city}'"
        query = query +';'
        payload = { #"ksql": "SELECT * FROM prova_x; ",
                    "ksql": f'{query}',
                    "streamsProperties": {}
                    }
        headers = {"Content-Type" : "application/vnd.ksql.v1+json; charset=utf-8"}
        req = requests.Request("POST","http://localhost:8088/query",
                               headers=headers,
                               data=json.dumps(payload)).prepare()

        resp = s.send(req, stream=True)

        for line in resp.iter_lines():
            if line:
                yield(line)


    def read_stream():
        for line in filtering('Firenze'):
            print(line)

    read_stream()

from Threading import Threading
import time
t = Threading()
time.sleep(2)
print(t.get_thread_status())
time.sleep(2)
t.terminate_thread()
time.sleep(0.1)
print(t.get_thread_status())
