from datetime import datetime


class Device(object):
    ip = None
    mac = None
    firstconnect = None
    lastconnect = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def create(ip, mac):
        return Device(ip=ip, mac=mac, firstconnect=datetime.now().strftime("%a, %H:%M:%S %d.%m.%Y"))
