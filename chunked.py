import requests
import json
"""
def gen():
    base_url = 'http://10.0.0.17:5000/time'
    r = requests.get(base_url, stream=True)
    buffer=""
    for chunk in r.iter_content(chunk_size=1):
        str_chunk = str(chunk)
        if str_chunk.endswith('\n'):
            buffer += str(chunk)
            yield(buffer)
            buffer = ""
        else:
            buffer += str(chunk)

for raw in gen():
    print(raw)
    try:
        boh = json.loads(raw)
        print(boh)
    except ValueError as e:
        print(e)
        continue
"""
base_url = 'http://127.0.0.1:5000/time'
r = requests.get(base_url, stream=True)
all_messages = []
for chunk in r.iter_content(decode_unicode=True):
    print(chunk)
    all_messages += str(chunk)
    print(all_messages)
