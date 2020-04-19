import dataset
from datetime import datetime
from Scany.libs.Device import Device


class DB(object):
    DATE_FORMAT = "%a, %H:%M:%S %d.%m.%Y"

    db = None
    devices = []

    def __init__(self, database="Scany.db"):
        self.db = dataset.connect('sqlite:///{0}'.format(database))

    def update(self, device):
        # print(device.__dict__)
        update_data = device.__dict__
        update_data["lastconnect"] = datetime.now().strftime("%a, %H:%M:%S %d.%m.%Y")
        self.db["devices"].upsert(update_data, ["mac"])

    def find(self, device):
        dev = self.db["devices"].find_one(mac=str(device.mac))
        if dev is None:
            return None
        del dev["id"]
        return Device(**dev)

    def get_all(self):
        r = []
        for dev in self.db["devices"].all():
            r.append(Device(**dev).__dict__)

        return r
