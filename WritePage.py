import tkinter as tk
import random
import requests
import json
from tkinter import messagebox
import geocoder
import reverse_geocoder as rg
import time

class WritePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.pages = controller.get_frames() # prende le pagine
        self.controller = controller

        # user creation
        # it does the following:
        # the first time that the page is shown, it triggers a funciton that
        # gets the user's username
        self.user_id = None
        self.location_list = ['Milano', 'Firenze', 'Roma','Napoli', 'Torino']
        self.n_times_shown = 0 # we'll use this to trigger the creation of the User at start
        self.bind("<<ShowFrame>>", self._on_first_show_frame) # binda all'evento, serve per dire quando viene mostrata

    def _on_first_show_frame(self, event):
        if self.n_times_shown == 0:
            self.user_id = self.controller.get_user_id()

            # label
            label = tk.Label(self, text=f"What's happening, {self.user_id}?", font=self.controller.title_font)
            label.pack(side="top", fill="x", pady=10)
            # text entry
            self.tweet_txt = tk.Entry(self,width=20)
            self.tweet_txt.pack()
            # publish button
            publish_btn = tk.Button(self, text="Publish!", command=self._publish, height="2", width="30").pack()
            back_btn = tk.Button(self, text="<- Back to Home", command=self._back_to_home, height="2", width="30").pack()
            self.n_times_shown =-1
        self._clear_text()

    def _publish(self):
        if self.tweet_txt.get()!='':

            payload = {
                'id': f'{self.user_id}',
                'content': self.tweet_txt.get(),
                'timestamp': time.time(),
                'location': random.choice(self.location_list)
            }

            r = requests.post("http://127.0.0.1:5000/tweet", data=payload)

            print('Tweet published!')
            self.controller.show_frame("HomePage")
            self._clear_text()
        else:
            messagebox.showerror("Whoops", "It seems that your tweet is empty... Write us something!")

    def _clear_text(self):
        self.tweet_txt.delete(0, 'end')

    def _reverseGeocode(self): # NOTE: unusable without internet connection...
        g = geocoder.ip('me')
        print(g.latlng)
        # coorinates tuple.Can contain more than one pair.
        coordinates =(g.latlng[0], g.latlng[1])
        result = rg.search(coordinates)
        # result is a list containing ordered dictionary
        return f"{result[0]['name']}, {result[0]['cc']}"

    def _back_to_home(self):
        self.is_shown = False
        self._clear_text()
        print('Back to Home.')
        self.controller.show_frame("HomePage")
