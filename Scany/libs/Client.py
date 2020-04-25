import hashlib
from threading import Thread, Timer
from getpass import getpass

import requests


class Client(Thread):
    dest = None
    passwd = None
    token = None
    t = None

    def __init__(self, dst, pwd, db):
        Thread.__init__(self)
        self.dest = dst
        self.passwd = hashlib.sha256(pwd.encode("UTF-8")).hexdigest()
        self.db = db

    def run(self) -> None:
        self.auth()

    def auth(self):
        d = self.dest + "/AuthClient"
        r = requests.post(d, json={"password": self.passwd}, timeout=100)
        # print(r.text)
        if r.status_code == requests.codes.ok:
            res = r.json()
            if res["resp"] == "None":
                print("Wrong password.")
                pwd = getpass()
                self.passwd = hashlib.sha256(pwd.encode("UTF-8")).hexdigest()
                self.auth()
            else:
                self.token = res["resp"]
                self.send()
        else:
            print("No connection")

    def send(self):
        d = self.dest + "/DB"
        data = {"token": self.token, "devices": self.db.get_all_devices()}
        r = requests.post(d, json=data)
        if r.status_code == requests.codes.ok:
            res = r.json()
            if res["resp"] == "wrongg":
                self.auth()
            else:
                print("sending now")
                t = Timer(300, self.send)
                t.start()
        else:
            r.raise_for_status()

    def stop(self):
        self.t.cancel()
