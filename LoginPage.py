import tkinter as tk
from TwitterUser import TwitterUser
import requests
import json
from tkinter import messagebox

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # default username
        self.username = ''
        label = tk.Label(self, text="Welcome to KafkaTwitter!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=50)
        # entry boxes
        name_label = tk.Label(self, text="Name:", font=controller.title_font).pack(side="top", fill="x", pady=5)
        self.name_box = tk.Entry(self,width=20)
        self.name_box.pack()
        surname_label = tk.Label(self, text="Surname:", font=controller.title_font).pack(side="top", fill="x", pady=5)
        self.surname_box = tk.Entry(self,width=20)
        self.surname_box.pack()
        psw_label = tk.Label(self, text="Password:", font=controller.title_font).pack(side="top", fill="x", pady=5)
        self.psw_box = tk.Entry(self,width=20, show='*')
        self.psw_box.pack()
        submit_btn = tk.Button(self, text="Login", command=self._submit, height="2", width="30").pack(pady=20)

    def _submit(self):
        if (self.name_box.get()!='') and (self.surname_box.get()!=''):
            self.username = self.name_box.get()
            self._login(self.name_box.get(), self.surname_box.get())
            self.controller.show_frame("HomePage")
        else:
            messagebox.showerror("Whoops", "It seems that your credentials are invalid or empty...")

    def _login(self, name, surname):
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
