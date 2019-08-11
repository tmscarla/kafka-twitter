import tkinter as tk
from TwitterUserAvro import TwitterUser
import requests
import json
from tkinter import messagebox
from PIL import ImageTk, Image

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.twitter_user = None

        #label = tk.Label(self, text="Welcome to KafkaTwitter!", font=controller.title_font)
        #label.pack(side="top", fill="x", pady=50)
        # carica logo
        img = Image.open("images/logo.png")
        w,h = img.size
        img_resized = img.resize((w//4,h//4), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img_resized)
        panel = tk.Label(self, image = image, background='white')
        panel.photo = image
        panel.pack(side='top',fill='both')
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
        submit_btn = tk.Button(self, text="Login",command=self._submit, height="2", width="30").pack(pady=20)

    def _submit(self):
        if (self.name_box.get()!='') and (self.surname_box.get()!=''):
            # user creation
            self.twitter_user = self._login(self.name_box.get(), self.surname_box.get())
            self.controller.set_twitter_user(self.twitter_user)
            # subscribe to topic
            self.twitter_user.subscribe_to_topic(self.controller.topic)
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
          "format": "avro",
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
