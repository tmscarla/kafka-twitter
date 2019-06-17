import tkinter as tk
from TwitterUser import TwitterUser
import requests
import json
from tkinter import messagebox

class WritePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="What's happening?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.tweet_txt = tk.Entry(self,width=20)
        self.tweet_txt.pack()

        publish_btn = tk.Button(self, text="Publish!", command=self._publish, height="2", width="30").pack()

    def _publish(self):
        if self.tweet_txt.get()!='':
            print('Tweet published!')
            self.controller.show_frame("HomePage")
            self._clear_text()
        else:
            messagebox.showerror("Whoops", "It seems that your tweet is empty... Write us something!")

    def _clear_text(self):
        self.tweet_txt.delete(0, 'end')
