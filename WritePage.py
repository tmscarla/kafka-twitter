import tkinter as tk
from TwitterUserAvro import TwitterUser
import requests
import json
from tkinter import messagebox

class WritePage(tk.Frame):

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

    def _on_first_show_frame(self, event):
        if self.n_times_shown == 0:
            self.twitter_user = self.controller.get_twitter_user()

            # label
            label = tk.Label(self, text=f"What's happening, {self.twitter_user.get_username()}?", font=self.controller.title_font)
            label.pack(side="top", fill="x", pady=10)
            # text entry
            self.tweet_txt = tk.Entry(self,width=20)
            self.tweet_txt.pack()
            # publish button
            publish_btn = tk.Button(self, text="Publish!", command=self._publish, height="2", width="30").pack()

            self.n_times_shown =-1
        self._clear_text()

    def _publish(self):
        if self.tweet_txt.get()!='':
            self.twitter_user.produce(self.controller.topic, self.tweet_txt.get())
            print('Tweet published!')
            self.controller.show_frame("HomePage")
            self._clear_text()
        else:
            messagebox.showerror("Whoops", "It seems that your tweet is empty... Write us something!")

    def _clear_text(self):
        self.tweet_txt.delete(0, 'end')
