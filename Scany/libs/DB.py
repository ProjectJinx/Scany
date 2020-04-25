import dataset
from datetime import datetime
from Scany.libs.Device import Device
from Scany.libs.Token import Token


class DB(object):
    DATE_FORMAT = "%a, %H:%M:%S %d.%m.%Y"

    db = None
    devices = []
    sleep = None

    def __init__(self, database="Scany.db", sleep=3600):
        self.db = dataset.connect('sqlite:///{0}'.format(database))
        self.sleep = sleep

    def update_device(self, device):
        update_data = device.__dict__
        update_data["lastconnect"] = datetime.now().strftime(self.DATE_FORMAT)
        self.db["devices"].upsert(update_data, ["mac"])

    def update_all_devices(self, devices):
        for d in devices:
            self.update_device(Device(**d))

    def find_device(self, device):
        dev = self.db["devices"].find_one(mac=str(device.mac))
        if dev is None:
            return None
        del dev["id"]
        return Device(**dev)

    def get_all_devices(self):
        r = []
        for dev in self.db["devices"].all():
            r.append(Device(**dev).__dict__)

        return r

    def update_token(self, token):
        update_data = token.__dict__
        update_data["lastconnect"] = datetime.now().strftime(self.DATE_FORMAT)
        self.db["tokens"].upsert(update_data, ["passwd"])

    def check_tokens(self):
        for tk in self.db["tokens"].all():
            # del tk["id"]
            t = Token(**tk)
            if ((datetime.now() - t.lastconnect).seconds / 60) >= self.sleep:
                self.db["tokens"].delete(passwd=t.passwd)

    def token_exists(self, passwd):
        tk = self.db["tokens"].find_one(passwd=passwd)
        if tk is None:
            return False
        else:
            # del tk["id"]
            tk = Token(**tk)
            self.update_token(tk)
        return True
