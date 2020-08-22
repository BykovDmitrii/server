from flask import Flask, request
import sqlite3
import json
import io
import uuid
from pydantic import BaseModel
import speech_recognition as sr

app = Flask(__name__)


def request_id_generator():
    from time import time
    from random import randint
    return hash(time() * 1000 + randint(-1000, 1000))


class Claim:
    def __init__(self, parsed_json):
        self.text = parsed_json["text"]
        self.email = parsed_json.get("email", "None")
        self.label = parsed_json.get("label", "None")
        self.api_name = parsed_json.get("api_name", "None")
        self.user_id = parsed_json.get("user_id", "None")
        self.request_id = str(request_id_generator())

    def calc_label(self):
        self.label = "xz"

    def send_to_subd(self):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Claims(request_id TEXT PRIMARY KEY, user_id TEXT, email TEXT, api_name TEXT, text TEXT, label TEXT, status TEXT)""")
        cursor.execute("""INSERT INTO Claims VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(self.request_id, self.user_id, self.email, self.api_name, self.text, self.label, "NEW"))
        cursor.close()
        conn.commit()


@app.route('/ourfront', methods=["POST"])
def from_our_front():
    claim = Claim(eval(request.data))
    claim.send_to_subd()
    return claim.request_id



@app.route('/api', methods=["POST"])
def from_api():
    claim = Claim(eval(request.data))
    claim.send_to_subd()
    return claim.request_id


def recognize(buffer: io.BytesIO, language='ru-RU') -> str:
    r = sr.Recognizer()
    with sr.AudioFile(buffer) as source:
        audio = r.record(source)  # read the entire audio file

    return r.recognize_google(audio, language='ru-RU')


class Item(BaseModel):
    audio: str

@app.route("/recognize", methods=["POST"])
def sound_from_api():
    data = eval(request.json['audio'])
    bytes_io = io.BytesIO(data)
    text = recognize(bytes_io)
    claim = Claim(dict(text=text))
    claim.send_to_subd()
    return claim.request_id


@app.route("/get_requests_by_user_id/<user_id>")
def get_user_requests(user_id):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cur = cursor.execute("""SELECT * FROM Claims WHERE user_id == '{}'""".format(user_id))
    rows = cur.fetchall()
    cursor.close()
    conn.commit()
    return tuple([row[0] for row in rows])


@app.route("/get_status_by_request_id/<request_id>")
def get_status(request_id):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cur = cursor.execute("""SELECT * FROM Claims WHERE request_id == '{}'""".format(request_id))
    rows = cur.fetchall()
    cursor.close()
    conn.commit()
    if len(rows) == 0:
        return "UNDEF"
    else:
        return rows[0][-1]

@app.route("/get_requests_with_status/<status>")
def get_next_request(status):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cur = cursor.execute("""SELECT * FROM Claims WHERE status == '{}'""".format(status))
    rows = cur.fetchall()
    cursor.close()
    conn.commit()
    return tuple([row[0] for row in rows])

if __name__ == "__main__":
    app.run(debug=True)
