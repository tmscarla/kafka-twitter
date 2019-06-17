import tkinter as tk
from TwitterUser import TwitterUser
import requests
import json


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Login Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        # entry boxes
        self.name_box = tk.Entry(self,width=20)
        self.name_box.pack()
        self.surname_box = tk.Entry(self,width=20)
        self.surname_box.pack()
        submit_btn = tk.Button(self, text="Login", command=self._submit, height="2", width="30").pack()

    def _submit(self):
        self.login(self.name_box.get(), self.surname_box.get())
        self.controller.show_frame("HomePage")

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
