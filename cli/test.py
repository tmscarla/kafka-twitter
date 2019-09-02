import requests

payload = {
    'consumer_name': 'Matteo',
    'user_tweet_id': 1,
    'message_text': 'ciao'
}

r = requests.post("http://127.0.0.1:5000/tweet", data=payload)
print(r.text)
