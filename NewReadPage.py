import tkinter as tk
from TwitterUser import TwitterUser
import requests
import json
from tkinter import messagebox

class NewReadPage(tk.Frame):

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

        back_btn = tk.Button(self, text="<- Back to Home", command=self._back_to_home, height="2", width="30").pack()
        # scrollbar
        self.canvas = tk.Canvas(self)
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.frame = tk.Frame(self.canvas)
        # put the frame in the canvas
        self.canvas.create_window(0, 0, anchor='nw', window=self.frame)
        # make sure everything is displayed before configuring the scrollregion
        self.canvas.update_idletasks()

        self.canvas.configure(scrollregion=self.canvas.bbox('all'),
                         yscrollcommand=self.scroll_y.set)

        self.canvas.pack(fill='both', expand=True, side='left')
        self.scroll_y.pack(fill='y', side='right')

    def _on_first_show_frame(self, event):
        if self.n_times_shown == 0:
            self.twitter_user = self.pages['LoginPage'].get_user()
            self.n_times_shown =-1

        msgs = self.twitter_user.get_message()

        for m in msgs:
            display_msg = f"{m['key']}: {m['message']}"
            tk.Label(self.frame, justify='left',font=self.controller.title_font,
                    wraplength=450,
                    textvariable=m['message']).pack()

    def _back_to_home(self):
        print('Back to Home.')
        self.controller.show_frame("HomePage")
