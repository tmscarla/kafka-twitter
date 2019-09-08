import requests
import json

id = 'teo'

url=f"http://localhost:8082/consumers/{id}"

headers = {
"Content-Type" : "application/vnd.kafka.json.v2+json"
}

payload = {
  "name": f"{id}",
  "auto.offset.reset": "earliest",
  "auto.commit.enable": "true" # se metto a 'true' cancella i messaggi: va messo per il singolo consumer
}
r = requests.post(url, data=json.dumps(payload), headers=headers)
json_data = json.loads(r.text)
if 'error_code' in json_data:
    if json_data['error_code'] == 40902:
        print(f'Welcome back, {id}!')
else:
    print(f"We're creating your KafkaTwitter account, {id}!")

url = f'http://localhost:8082/consumers/{id}/instances/{id}/subscription'
headers = {
"Content-Type" : "application/vnd.kafka.json.v2+json"
}
payload = {
  "topics": [
    "__current_offsets"
  ]
}
r = requests.post(url, data=json.dumps(payload), headers = headers)
print(r)

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
