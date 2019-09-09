import requests
import time

base_url = 'http://10.0.0.17:5000/'
"""
# session creation
s = requests.Session()

# subscribe + cookie creation
specific_url = 'users/id'
id = 'xxx'
data = {'id':id}
cookies={'username': id, 'page': ''}
r = requests.post(base_url+specific_url,data=data)
print(r.text)
"""
# post
import geocoder
import reverse_geocoder as rg
def _reverseGeocode():
    g = geocoder.ip('me')
    print(g.latlng)
    # coorinates tuple.Can contain more than one pair.
    coordinates =(g.latlng[0], g.latlng[1])
    result = rg.search(coordinates)
    # result is a list containing ordered dictionary
    return f"{result[0]['name']}, {result[0]['cc']}"
location = 'Firenze'
specific_url = 'tweet'
for i in range(5):
    id = i
    time.sleep(1)
    data = {
        'id': i, #questo non deve passarlo
        'content': f'come va? #{i} @ciao',
        "timestamp": time.time(),
        'location': location
    }
    r = requests.post(base_url+specific_url,data=data)
    print(r.text)
"""
# read
cookies['page'] = 'read'
specific_url_1 = 'tweets/nofilters/latest'
specific_url_2 = 'tweets/mentionfilter=cia0o/latest'
r = requests.get(base_url+specific_url_1, cookies=cookies)
for m in r.json()['results']:
    print(m)
# stream
cookies['stream'] = 'stream'
"""
