def login(self, name, surname):
        url=f"http://localhost:8082/consumers/{surname}"

        headers = {
        "Content-Type" : "application/vnd.kafka.json.v2+json"
        }

        payload = {
          "name": f"{name}",
          "format": "binary",
          "auto.offset.reset": "earliest",
          "auto.commit.enable": "true" # se metto a 'true' cancella i messaggi: va messo per il singolo consumer
        }
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        json_data = json.loads(r.text)
        if 'error_code' in json_data:
            if json_data['error_code'] == 40902:
                print(f'Welcome back, {name}!')
        else:
            print(f"We're creating your KafkaTwitter account, {name}!")
        return TwitterUser(name, surname)
