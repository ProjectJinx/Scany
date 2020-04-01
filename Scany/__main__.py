#!/usr/bin/python3
from argparse import ArgumentParser
from getpass import getpass

from Scany import *


def main():
    p = ArgumentParser()
    p.add_argument("-s", "--server", action="store_true", help="start the http api server")
    p.add_argument("-db", "--database", type=str, default="Scany.db", help="path to sqlite database")
    p.add_argument("--sleep", type=int, default=10, help="sleep time for scanner")

    a = p.parse_args()
    db = DB(a.database)

    tasks = []
    if a.server:
        pw = getpass()
        tasks.append(Server(pw, db))

    tasks.append(Scanner(db, a.sleep))

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
