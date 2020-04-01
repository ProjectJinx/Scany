from time import sleep
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM
from scapy.layers.l2 import Ether, ARP
from scapy.all import srp

from Scany.libs.Device import Device


class Scanner(Thread):
    running = False
    daemon = True
    ip = None
    subnet = None
    db = None

    @staticmethod
    def get_local_ip(remote_host="8.8.8.8", remote_port=80):
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect((remote_host, remote_port))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def __init__(self, db, sleep_time=10, **kwargs):
        Thread.__init__(self)
        self.sleep_time = sleep_time
        self.ip = self.get_local_ip(kwargs.get("remote_host") or "8.8.8.8", kwargs.get("remote_port") or 80)
        self.subnet = self.ip[:self.ip.rfind(".")] + ".0/24"
        self.db = db
        self.running = True

    def run(self):
        while self.running:
            a, u = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.subnet), timeout=2)
            for a in a:
                dev = Device.create(a[1][Ether].psrc, a[1][Ether].src, self.db.DATE_FORMAT)
                self.db.update(self.db.find(dev) or dev)
            sleep(self.sleep_time)

    def stop(self):
        self.running = False


if __name__ == '__main__':
    def check(addr):
        if isinstance(addr, str):
            addr.split(":")
        s = Scanner(None, remote_host=addr[0], remote_port=int(addr[1]))
        print(':'.join(addr), s.ip)
    check("8.8.8.8:80")
    check("127.0.0.1:53")
    check("eberlein.io:80")
