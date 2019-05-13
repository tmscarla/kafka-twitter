key_schema = open("my_key.avsc", 'rU').read()
value_schema = open("my_value.avsc", 'rU').read()

producerurl = "http://kafkarest1:8082/topics/my_avro_topic"
headers = {
"Content-Type" : "application/vnd.kafka.avro.v1+json"
}
payload = {
"key_schema": key_schema,
"value_schema": value_schema,
"records":
[{
"key": {"suit": "spades"},
"value": {"suit": "spades", "card": "ace"}
}]}
# Send the message
r = requests.post(producerurl, data=json.dumps(payload), headers=headers)
if r.status_code != 200:
    print("Status Code: " + str(r.status_code))
    print(r.text)
