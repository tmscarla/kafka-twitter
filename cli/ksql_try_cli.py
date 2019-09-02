import requests
import json

# <path-to-confluent>/bin/confluent local start
# urls
base_url = "http://0.0.0.0:8088/ksql"
query_url = "http://localhost:8088/query"


# create ksql stream
"""
headers = {
    "Content-Type" : "application/vnd.ksql.v1+json",
    "Accept" : "application/vnd.ksql.v1+json"
}

payload = {
    "ksql": "CREATE STREAM prova_x WITH (KAFKA_TOPIC='provaksql',VALUE_FORMAT='AVRO');",
    "streamsProperties": {
      "ksql.streams.auto.offset.reset": "earliest"
    }

}

r = requests.post(base_url, data=json.dumps(payload), headers=headers)
print(r.text)
"""

# read ksql
s = requests.Session() # session creation

def filtering(city = None):
    query = "SELECT * FROM prova_4"
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
