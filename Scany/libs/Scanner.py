#!/usr/bin/python3
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM
from scapy.layers.l2 import Ether, ARP
from scapy.all import srp
from time import sleep
from Scany.libs.Device import Device


class Scanner(Thread):
    running = False
    daemon = True
    ip = None
    ips = None
    db = None

    def __init__(self, db, sleeptime=10):
        Thread.__init__(self)
        self.running = True
        self.sleeptime = sleeptime
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ip = s.getsockname()[0]
        s.close()
        self.ips = self.ip[:self.ip.rfind(".")] + ".0/24"
        self.db = db

    def run(self):
        while self.running:
            ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.ips), timeout=2)
            for a in ans:
                dev = Device.create(a[1][Ether].psrc, a[1][Ether].src)  # psrc = IP Address / src = MAC Address
                self.db.update_device(self.db.find_device(dev) or dev)
            sleep(self.sleeptime)

    def stop(self):
        self.running = False
