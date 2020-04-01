from Scanner import Scanner
from argparse import ArgumentParser
from Server import Server
from getpass import getpass
from DB import DB


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument("-s", "--server", action="store_true")
    p.add_argument("--sleep", type=int, default=10)
    p.add_argument("-db", "--database", type=str, default="Scany.db")

    a = p.parse_args()
    db = DB(a.database)
    if a.server:
        pw = getpass()
        srv = Server(pw, db)
        srv.start()

    scn = Scanner(db, a.sleep)
    try:
        scn.start()
        scn.join()
    except KeyboardInterrupt:
        scn.stop()
