# read ksql
import threading
import requests
import json
import datetime
import time
import multiprocessing

class Threading(object):
    def __init__(self, request):
        self.r = request
        self.thread = threading.Thread(target=self.streaming, args=())
        self.thread.daemon = True
        self.thread.start()

    def terminate_thread(self):
        self.thread.terminate()

    def get_thread_status(self):
        return self.thread.is_alive()

    def get_msg_list(self):
        if len(self.msg_list) !=0:
            ts = time.time()
            self.msg_list = [x for x in self.msg_list if (ts-float(x[2]))<10]
            return self.msg_list

    def streaming(self):
        msg_string = ""
        # the entire msg list to display
        # this one is useful to split the strings finding starting and final byte
        is_start=True
        for c in self.r.iter_content(decode_unicode=True):
            if (c):
                if str(c) =='`' and is_start==True:
                    msg_string =''
                    is_start = False
                elif str(c) =='`' and is_start==False:
                    msgs = json.loads(msg_string) # bc it's a string representation of a list
                    self._destroy_msg_list()
                    for m in msgs:
                        self.msg_list.insert('end',m)
                    self.msg_list.pack(pady=5)
                    is_start=True
                else:
                    msg_string += str(c)

self.thread = threading.Thread(target=self.streaming, args=(r,))
