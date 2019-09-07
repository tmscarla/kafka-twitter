from flask import Flask, request, session
import os

app = Flask(__name__)

@app.route('/')
def f_index():
    # Request Headers, sent on every request
    print("\n\n\n[Client-side]\n", request.headers)
    if 'visits' in session:
        # getting value from session dict (Server-side) and incrementing by 1
        session['visits'] = session.get('visits') + 1
    else:
        # first visit, generates the key/value pair {"visits":1}
        session['visits'] = 1
        # 'session' cookie tracked from every request sent
        print("[Server-side]\n", session)
    return "Total visits:{0}".format(session.get('visits'))


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run()
