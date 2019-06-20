import tkinter as tk
from TwitterUser import TwitterUser
import requests
import json
from tkinter import messagebox

class ReadPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.pages = controller.get_frames() # prende le pagine
        self.controller = controller

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
        self.scrollbar.config(command = self.msg_list.yview )



    def _on_first_show_frame(self, event):
        if self.n_times_shown == 0:
            self.twitter_user = self.controller.get_twitter_user()

            # label
            label = tk.Label(self, text=f"{self.twitter_user.get_username()}, these are the latest tweets", font=self.controller.title_font)
            label.pack(side="top", fill="x", pady=10)

            back_btn = tk.Button(self, text="<- Back to Home", command=self._back_to_home, height="2", width="30").pack()
            self.n_times_shown =-1

        msgs = self.twitter_user.get_message()

        for m in msgs:
            display_msg = f"{m['key']}: {m['message']} "
            self.msg_list.insert(0,display_msg)
            self.msg_list.insert(0,"=====================================================")

        self.msg_list.pack(pady=5)#(side = 'right', fill='both', pady=10)

    def _back_to_home(self):
        print('Back to Home.')
        self.controller.show_frame("HomePage")
