import requests
import json
"""
payload = {
    'consumer_name': 'Matteo',
    'user_tweet_id': 1,
    'message_text': 'forza inter! #inter #fcim1908',
}

r = requests.post("http://127.0.0.1:5000/tweet", data=payload)
print(r.text)
"""
url = f'http://localhost:8082/consumers/c/instances/c/positions'
headers = {
"Content-Type" : "application/vnd.kafka.json.v2+json"
}
payload = {
  "offsets": [{
    "topic" : "test_kf_s",
    "partition": 0,
    "offset": 37}
  ]
}
r = requests.post(url, data=json.dumps(payload), headers = headers)
print(r.text)
