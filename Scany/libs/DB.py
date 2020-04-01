import dataset
from datetime import datetime
from Scany.libs.Device import Device


class DB(object):
    DATE_FORMAT = "%a, %H:%M:%S %d.%m.%Y"

    TABLE_DEVICES = "devices"
    COLUMN_DEVICE_ID = "id"
    COLUMN_DEVICE_MAC = "mac"

    db = None
    devices = []

    def __init__(self, database="Scany.db"):
        self.db = dataset.connect('sqlite:///{0}'.format(database))

    def update(self, device):
        device.last_connect = datetime.now().strftime(self.DATE_FORMAT)
        self.db[self.TABLE_DEVICES].upsert(device.__dict__, [self.COLUMN_DEVICE_MAC])

    def find(self, device):
        dev = self.db[self.TABLE_DEVICES].find_one(mac=str(device.mac))
        if dev is None:
            return None
        del dev[self.COLUMN_DEVICE_ID]
        return Device(**dev)

    def get_all(self):
        r = []
        for dev in self.db[self.TABLE_DEVICES].all():
            r.append(Device(**dev).__dict__)
        return r
