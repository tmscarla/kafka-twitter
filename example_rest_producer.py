import requests
import base64
import json


"""
PRIMA DI RUNNARE, in confluent da cmd:

./bin/zookeeper-server-start ./etc/kafka/zookeeper.properties
./bin/kafka-server-start ./etc/kafka/server.properties
./bin/schema-registry-start ./etc/schema-registry/schema-registry.properties
./bin/kafka-rest-start ./etc/kafka-rest/kafka-rest.properties

"""
url="http://localhost:8082/topics/ex"
headers= {"Content-Type":"application/vnd.kafka.v2+json",
"Accept": "application/vnd.kafka.v2+json"}

payload={'records': [{
        'key': 'firstkey',
        'value': 'firstvalue'
        }]}

r=requests.post(url,data=json.dumps(payload),headers=headers)
print(r.text)

if r.status_code !=200:
    print('Status Code : {}'.format(r.status_code))
    print(r.text)
