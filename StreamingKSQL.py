import tkinter as tk
import threading
import requests
import json
import datetime
from tkinter import messagebox

class StreamingKSQL(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.pages = controller.get_frames() # prende le pagine
        self.controller = controller
        self.is_shown = False
        # user creation
        self.user_id = None
        self.streaming_url = 'http://127.0.0.1:5000/tweets/streaming'
        self.n_times_shown = 0 # we'll use this to trigger the creation of the User at start
        self.bind("<<ShowFrame>>", self._on_first_show_frame) # binda all'evento, serve per dire quando viene mostrata

        # filter entries
        city_label = tk.Label(self,text="city filter:", font=self.controller.title_font).pack(side="top")
        self.cf = tk.Entry(self, width=20)
        self.cf.pack()

        mention_label = tk.Label(self,text="mention filter:", font=self.controller.title_font).pack(side="top")
        self.mf = tk.Entry(self, width=20)
        self.mf.pack()

        tag_label = tk.Label(self,text="tag filter:", font=self.controller.title_font).pack(side="top")
        self.tf = tk.Entry(self, width=20)
        self.tf.pack()

        # scrollbar
        self.scrollbar =  tk.Scrollbar(self)
        self.scrollbar.pack(side = 'left', fill='y')
        self.msg_list = tk.Listbox(self, height="70",width="50", yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.msg_list.yview)

    def get_is_shown(self):
        return self.is_shown

    def _on_first_show_frame(self, event):
        if self.n_times_shown == 0:
            self.user_id = self.controller.get_user_id()

            # label
            label = tk.Label(self, text=f"{self.user_id}, these are the latest tweets", font=self.controller.title_font)
            label.pack(side="top", fill="x", pady=10)
            stream = tk.Button(self, text="Read Messages!", command=self._stream, height="2", width="30").pack()
            back_btn = tk.Button(self, text="<- Back to Home", command=self._back_to_home, height="2", width="30").pack()
            self.n_times_shown =-1

        self.is_shown = True

    def _stream(self):
        self._destroy_msg_list()

        # convert all to lower case
        cityfilter = self.cf.get().lower()
        mentionfilter = self.mf.get().lower()
        tagfilter = self.tf.get().lower()

        # if no filter is applied, select all city/mention/tag
        if cityfilter=='':
            cityfilter = 'ALL'
        if mentionfilter=='':
            mentionfilter = 'ALL'
        if tagfilter=='':
            tagfilter = 'ALL'

        payload = {
            'cityfilter': cityfilter,
            'mentionfilter': mentionfilter,
            'tagfilter': tagfilter
        }
        cookies={'username': self.user_id}

        r = requests.post(self.streaming_url, data=payload, cookies=cookies, stream=True)
        msg_string = ""
        msg_list = []

        is_start=True
        for c in r.iter_content(decode_unicode=True):
            if (c):
                if str(c) =='`' and is_start==True:
                    msg_string =''
                    is_start = False
                elif str(c) =='`' and is_start==False:
                    print(json.loads(msg_string))
                    is_start=True
                else:
                    msg_string += str(c)
            else:
                print('===')

    def _stream_response(self, r):
        # single string message
        msg_string = ""
        # the entire msg list to display
        # this one is useful to split the strings finding starting and final byte
        is_start=True
        for c in r.iter_content(decode_unicode=True):
            if (c):
                if str(c) =='`' and is_start==True:
                    msg_string =''
                    is_start = False
                elif str(c) =='`' and is_start==False:
                    msgs = json.loads(msg_string) # bc it's a string representation of a list
                    #self._destroy_msg_list()
                    print(msgs)
                    #for m in msgs:
                    #    self.msg_list.insert('end',m)
                    self.msg_list.pack(pady=5)
                    is_start=True
                else:
                    msg_string += str(c)

    def _destroy_msg_list(self):
        self.msg_list.delete('0', 'end')

    def _back_to_home(self):
        self.is_shown = False
        print('Back to Home.')
        self.controller.show_frame("HomePage")
