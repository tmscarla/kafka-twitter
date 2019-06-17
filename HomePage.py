import tkinter as tk
from TwitterUser import TwitterUser
import requests
import json

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="What do you want to do?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        read_button = tk.Button(self, text="Read", command=self._read, height="2", width="30").pack()
        write_button = tk.Button(self, text="Write", command=self._write, height="2", width="30").pack()

    def _read(self):
        print('Reading!')

    def _write(self):
        print('Ok, write something!')
        self.controller.show_frame("WritePage")
