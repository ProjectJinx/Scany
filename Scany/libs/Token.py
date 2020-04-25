from datetime import datetime


class Token(object):
    passwd = None
    lastconnect = None
    date_format = "%a, %H:%M:%S %d.%m.%Y"

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.lastconnect = datetime.strptime(self.lastconnect, self.date_format)

    @staticmethod
    def create(password, date_format="%a, %H:%M:%S %d.%m.%Y"):
        return Token(passwd=password, lastconnect=datetime.now().strftime(date_format))
