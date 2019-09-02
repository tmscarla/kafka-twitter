import tkinter as tk
from TwitterUser import TwitterUser
import requests
import json
import datetime
from tkinter import messagebox

class StreamingReadPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.pages = controller.get_frames() # prende le pagine
        self.controller = controller
        self.is_shown = False
        # user creation
        # it does the following:
        # the first time that the page is shown, it triggers a funciton that
        # gets the user's username
        self.twitter_user = None
        self.n_times_shown = 0 # we'll use this to trigger the creation of the User at start
        self.bind("<<ShowFrame>>", self._on_first_show_frame) # binda all'evento, serve per dire quando viene mostrata
        # scrollbar
        self.scrollbar =  tk.Scrollbar(self)
        self.scrollbar.pack(side = 'left', fill='y')
        self.msg_list = tk.Listbox(self, height="70",width="50",yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.msg_list.yview)

    def get_is_shown(self):
        return self.is_shown

    def _on_first_show_frame(self, event):
        if self.n_times_shown == 0:
            self.twitter_user = self.controller.get_twitter_user()

            # label
            label = tk.Label(self, text=f"{self.twitter_user.get_username()}, these are the latest tweets", font=self.controller.title_font)
            label.pack(side="top", fill="x", pady=10)

            back_btn = tk.Button(self, text="<- Back to Home", command=self._back_to_home, height="2", width="30").pack()
            self.n_times_shown =-1

        self.is_shown = True
        self._get_msg_list_resc()

    def _get_msg_list(self):
        msgs = self.twitter_user.get_message()

        for m in msgs:
            # transform timestamp to a better readable format
            #msg_ts = datetime.datetime.fromtimestamp(float(m['value']['timestamp'])).strftime('%H:%M:%S, %d-%m-%Y')
            #display_msg = f"{m['value']['author']}: {m['value']['content']} ({msg_ts})"
            self.msg_list.insert(0,m)
            #self.msg_list.insert(0,"=====================================================")

        self.msg_list.pack(pady=5)
        #print(f"{self.msg_list.get(0, self.msg_list.size())}")

    def _get_msg_list_resc(self): # _get_msg_list rescheduled
        if self.is_shown == True: # altrimenti non ha senso che continui a fare richieste
            self._get_msg_list()
            self.after(1000, self._get_msg_list_resc)

    def _back_to_home(self):
        self.is_shown = False
        print('Back to Home.')
        self.controller.show_frame("HomePage")
