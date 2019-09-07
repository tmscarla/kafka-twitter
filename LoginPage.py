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
        name_label = tk.Label(self, text="Username:", font=self.controller.title_font).pack(side="top", fill="x", pady=5)
        self.name_box = tk.Entry(self,width=20)
        self.name_box.pack()
        # for the moment just comment this
        """
        surname_label = tk.Label(self, text="Surname:", font=controller.title_font).pack(side="top", fill="x", pady=5)
        self.surname_box = tk.Entry(self,width=20)
        self.surname_box.pack()
        psw_label = tk.Label(self, text="Password:", font=controller.title_font).pack(side="top", fill="x", pady=5)
        self.psw_box = tk.Entry(self,width=20, show='*')
        self.psw_box.pack()
        """
        submit_btn = tk.Button(self, text="Login",command=self._submit, height="2", width="30").pack(pady=20)

    def _submit(self):
        #if (self.name_box.get()!='') and (self.surname_box.get()!=''): uncomment ?
        if (self.name_box.get()!=''):
            # user subscription
            payload = {
                'id': f'{self.name_box.get()}'
            }
            # login + subscribe to topic REST post request
            r = requests.post("http://127.0.0.1:5000/users/id", data=payload)

            # twitter user creation
            self.twitter_user = TwitterUser(self.name_box.get())
            self.controller.set_twitter_user(self.twitter_user)

            # show HomePage
            self.controller.show_frame("HomePage")

        else:
            messagebox.showerror("Whoops", "It seems that your credentials are invalid or empty...")
