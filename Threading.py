# read ksql
import threading
import requests
import json
import datetime
import time
import multiprocessing

class Threading(object):
    def __init__(self):
        self.output_topic = 'test_kf_s'
        self.msg_list = []
        self.thread = multiprocessing.Process(target=self.streaming, args=())
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
        s = requests.Session() # session creation

        def filtering(city = None):
            query = f"SELECT author, content, timestamp FROM {self.output_topic}"
            if city:
                query = query + f" WHERE location LIKE '{city}'"
            query = query +f';'
            payload = {
                        "ksql": f'{query}',
                        "streamsProperties": {}
                        }
            headers = {"Content-Type" : "application/vnd.ksql.v1+json; charset=utf-8"}
            req = requests.Request("POST","http://localhost:8088/query",
                                   headers=headers,
                                   data=json.dumps(payload)).prepare()

            resp = s.send(req, stream=True)
            for line in resp.iter_lines(decode_unicode=True):
                if line:
                    yield(json.loads(line))


        def read_stream():
            for line in filtering('Firenze'):
                author = line['row']['columns'][0]
                content = line['row']['columns'][1]
                timestamp = line['row']['columns'][2] # datetime.datetime.fromtimestamp(float(line['row']['columns'][2])).strftime('%H:%M:%S, %d-%m-%Y')
                self.msg_list.append([author,content,timestamp])

        read_stream()
