import requests
import base64
import json
import sys

baseurl="http://localhost:8082/consumers/my_json_consumer"

name = 'my_consumer5'
payload = {
"name":name,
"format": "json",
"auto.offset.reset": "earliest"
}
headers = {
"Content-Type" : "application/vnd.kafka.v2+json"
}

r = requests.post(baseurl, data=json.dumps(payload), headers=headers)
print(r.text)
if r.status_code != 200:
    print("Status Code: " + str(r.status_code))
    print(r.text)
    sys.exit("Error thrown while creating consumer")


headers = {"Content-Type: application/vnd.kafka.v2+json"}
payload = {"topics":["jsontest"]}
url = f"http://localhost:8082/consumers/my_json_consumer/instances/{name}/subscription"
r = requests.post(url, data=json.dumps(payload), headers=headers)
print(r)
headers = {"Accept: application/vnd.kafka.json.v2+json"}
url = f"http://localhost:8082/consumers/my_json_consumer/instances/{name}/records"
r = requests.get(url, headers=headers)
print(r)
headers = {"Content-Type: application/vnd.kafka.v2+json"}
url = f"http://localhost:8082/consumers/my_json_consumer/instances/{name}"
r = requests.delete(url, headers=headers)
print(r)
