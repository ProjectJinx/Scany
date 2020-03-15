from threading import Thread
from flask import Flask, make_response, request as req
from werkzeug.serving import make_server
from json import dumps
from DB import DB


class Server(Thread):
    passwd = None
    app = None
    srv = None
    db = None

    def __init__(self, pwd, db):
        Thread.__init__(self)
        self.passwd = pwd
        self.app = Flask(__name__)
        self.srv = make_server("127.0.0.1", 1337, self.app)
        self.db = db

    def run(self) -> None:
        @self.app.route("/Scanner", methods=["GET", "POST"])
        def res():
            print(req.args)
            if req.method == "POST":
                print(req.json)
                if req.json["password"] == self.passwd:
                    devices = self.db.get_all()
                    return make_response(dumps(devices))
                else:
                    return make_response("no")
            else:
                return make_response("nono")

        self.srv.serve_forever()

    def stop(self):
        self.srv.shutdown()


if __name__ == '__main__':
    s = Server("Ananas", DB())
    s.start()
    s.join()
