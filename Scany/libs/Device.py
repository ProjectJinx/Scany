from datetime import datetime


class Device(object):
    ip = None
    mac = None
    first_connect = None
    last_connect = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def create(ip, mac, date_format="%a, %H:%M:%S %d.%m.%Y"):
        return Device(ip=ip, mac=mac, firstconnect=datetime.now().strftime(date_format))
