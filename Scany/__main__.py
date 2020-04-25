from argparse import ArgumentParser
from getpass import getpass
from Scany import *


def main():
    p = ArgumentParser()
    p.add_argument("-s", "--server", action="store_true", help="start the http api server")
    p.add_argument("--sleep", type=int, default=10, help="sleep time for scanner")
    p.add_argument("-db", "--database", type=str, default="Scany.db", help="path to sqlite database")
    p.add_argument("-c", "--client", action="store_true", default=True, help="start the client")
    p.add_argument("-u", "--URL", type=str, default="http://127.0.0.1:1337", help="destination for the client. Needs to include URL/IP + Port")
    p.add_argument("-scn", "--scan", action="store_true", help="scan only")

    tasks = []
    a = p.parse_args()
    db = DB(a.database)

    if a.server:
        pw = getpass()
        tasks.append(Server(pw, db))
    elif a.scan:
        tasks.append(Scanner(db, a.sleep))
    else:
        dst = a.URL
        pw = getpass()
        tasks.append(Scanner(db, a.sleep))
        tasks.append(Client(dst, pw, db))

    for task in tasks:
        task.start()
    try:
        tasks[0].join()
    except KeyboardInterrupt:
        for task in tasks:
            task.stop()
            task.join()


if __name__ == '__main__':
    main()
