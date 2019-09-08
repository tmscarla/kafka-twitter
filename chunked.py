import requests
import json
import time


# session creation
s = requests.Session()

# subscribe + cookie creation
base_url = 'http://127.0.0.1:5000/'
specific_url = 'users/id'
id = 'l'
data = {'id':id}
cookies={'username': id}
r = requests.post(base_url+specific_url,data=data)
print(r.text)
payload={
    'cityfilter':'',
    'mentionfilter':'',
    'tagfilter':''
}
r = requests.post('http://127.0.0.1:5000/tweets/streaming', data=payload,cookies=cookies, stream=True)
msg_string = ""
msg_list = []

is_start=True
for c in r.iter_content(decode_unicode=True):
    ts = time.time()
    if (c):
        if str(c) =='`' and is_start==True:
            msg_string =''
            is_start = False
        elif str(c) =='`' and is_start==False:
            print(json.loads(msg_string))
            is_start=True
        else:
            msg_string += str(c)
    else:
        print('===')
