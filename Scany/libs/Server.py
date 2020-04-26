import hashlib
import random
import string
from json import dumps
from threading import Thread, Timer

from flask import Flask, make_response, request as req
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.serving import make_server

from Scany.libs.Token import Token


def create_token():
    t = "".join(random.choices(string.ascii_letters + string.digits, k=500))
    t = "" + generate_password_hash(t)
    return t


class Server(Thread):
    passwd = None
    app = None
    srv = None
    db = None
    t = None

    def __init__(self, pwd, db):
        Thread.__init__(self)
        self.passwd = hashlib.sha256(pwd.encode("UTF-8")).hexdigest()
        self.app = Flask(__name__)
        self.srv = make_server("127.0.0.1", 1337, self.app)
        self.db = db
        print("initializing")

    def run(self) -> None:
        @self.app.route("/Auth", methods=["POST"])
        def auth():
            data = req.data.decode("utf-8").lower().replace('"', '')
            print("data = " + data)
            print("pass = " + self.passwd)
            print(self.passwd.__class__)
            if data == self.passwd:
                tk = Token.create(create_token())
                self.db.update_token(tk)
                print("pass = " + tk.passwd)
                return make_response(tk.passwd)
            else:
                print("Now I'm not doing it")
                return make_response("None")

        @self.app.route("/Scanner", methods=["GET", "POST"])
        def resp():
            print(req.data)
            if req.method == "POST":
                if self.db.token_exists(req.data):
                    print("sending devices")
                    return make_response(dumps({"devices": self.db.get_all_devices()}))
                else:
                    print("I dont like u")
                    return make_response("no thx")
            else:
                return make_response("what are u doing")

        @self.app.route("/AuthClient", methods=["POST"])
        def auth_client():
            if "password" in req.json.keys():
                if check_password_hash(req.json["password"], self.passwd):
                    tk = Token.create(create_token())
                    self.db.update_token(tk)
                    return make_response(dumps({"resp": tk.passwd}))
                else:
                    return make_response(dumps({"resp": "None"}))

        @self.app.route("/DB", methods=["POST"])
        def receive_db():
            if req.method == "POST":
                print(req.json)
                if "token" in req.json.keys():
                    if self.db.token_exists(req.json["token"]):
                        self.db.update_all_devices(req.json["devices"])
                        return make_response(dumps({"resp": "ok"}))
                else:
                    return make_response(dumps({"resp": "wrongg"}))
            else:
                return make_response(dumps({"resp": "???"}))

        self.check_token()
        print("now running")
        self.srv.serve_forever()

    def check_token(self):
        self.db.check_tokens()
        t = Timer(3600, self.check_token)
        t.start()

    def stop(self):
        self.srv.shutdown()
        self.t.cancel()
