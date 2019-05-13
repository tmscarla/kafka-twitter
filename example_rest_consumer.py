import requests
import base64
import json
import sys

baseurl="http://localhost:8082/consumers/group1"

payload = {
"format": "json"
}
headers = {
"Content-Type" : "application/vnd.kafka.v2+json"
}

r = requests.post(baseurl, data=json.dumps(payload), headers=headers)

if r.status_code != 200:
    print("Status Code: " + str(r.status_code))
    print(r.text)
    sys.exit("Error thrown while creating consumer")

# Base URI is used to identify the consumer instance
base_uri = r.json()["base_uri"]
print(base_uri)
# Get the message(s) from the Consumer
headers = {
"Accept" : "application/vnd.kafka.v2+json"
}
# Request messages for the instance on the Topic
r = requests.get(base_uri + "/topics/ex", headers=headers, timeout=20)

print(r)
if r.status_code != 200:
    print("Status Code: " + str(r.status_code))
    print(r.text)
    sys.exit("Error thrown while getting message")

# Output all messages
for message in r.json():
    if message["key"] is not None:
        print("Message Key:" + message["key"])
    print("Message Value:" + message["value"])

# When we're done, delete the Consumer
headers = {
    "Accept" : "application/vnd.kafka.v2+json"
}

r = requests.delete(base_uri, headers=headers)

if r.status_code != 204:
    print("Status Code: " + str(r.status_code))
    print(r.text)
