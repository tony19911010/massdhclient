from threading import Thread
import random
from time import time
#from scapy.all import srp, sendp, mac2str, srp1, sr1, conf, Ether
#from scapy.layers.dhcp import *
from scapy.all import *
from netaddr import EUI, mac_unix
import logging

conf.checkIPaddr = False
conf.verb = False


class DHCPClient:
    """
    loop and send Discovers
    """
    def __init__(self, iface, mac="00:00:5e:fa:00:00", hostname="C000001"):
        self.kill_received = False
        self.iface = iface
        self.state = 'born'
        self.time = time.time()
        self.mac = mac
        self.mac_str = mac2str(mac)
        self.hostname = hostname
        self.server_ip = None
        self.ip = None
        self.renew_time = None
        self.log = logging.getLogger(f"massdhclient.cl({self.hostname})")

    @property
    def req_options(self):
        return [
            ("message-type", "request"),
            ("server_id", self.server_ip),
            ("requested_addr", self.ip),
            ("client_id", chr(1), self.mac_str),
            ("hostname", self.hostname),
            ("end",'00000000000000')
        ]

    def discover(self):
        try:
            self.log.debug(f"Discover being sent")
            x_id = random.randrange(1, 1000000)
            disc_opts = [
                ("message-type", "discover"),
                ("client_id", chr(1), self.mac_str),
                ("hostname", self.hostname),
                ("end",'00000000000000')
            ]
            pkt = Ether(dst="ff:ff:ff:ff:ff:ff", src=self.mac) / IP(src="0.0.0.0", dst="255.255.255.255") / UDP(
                sport='bootpc', dport='bootps') / BOOTP(op='BOOTREQUEST', xid=x_id, chaddr=self.mac_str) / DHCP(
                options=disc_opts)
            t1 = time.time()
            resp = srp1(pkt, iface=self.iface, timeout=2.5, multi=True)
            self.ip = resp[1][BOOTP].yiaddr
            self.server_ip = resp[1][BOOTP].siaddr
            self.log.debug(f"Received offer for {self.ip} from {self.server_ip} in {time.time()-t1} seconds")

            req = Ether(dst="ff:ff:ff:ff:ff:ff", src=self.mac) / IP(src="0.0.0.0", dst="255.255.255.255") / UDP(
                sport=68, dport=67)/BOOTP(op="BOOTREQUEST", xid=x_id, chaddr=self.mac_str) / DHCP(options=self.req_options)
            t15 = time.time()
            resp = srp1(req, iface=self.iface, timeout=2.5, verbose=0)
            t2 = time.time()
            self.log.debug(f"Received ACK for {self.ip} from {self.server_ip} in {t2-t15} seconds")
            self._parse_renewal_time(resp, t2)
            return t2-t1
        except Exception as e:
            self.log.debug(f"Discover/ack failed: {str(e)}")
            return e

    def _parse_renewal_time(self, resp, t2):
        for tp in resp[1][DHCP].options:
            if not isinstance(tp, tuple):
                continue
            opt, value = tp
            if opt == 'renewal_time':
                self.renew_time = t2 + int(value)
                break
        else:
            raise ValueError(f"Unable to find renewal time in response: {resp[1][DHCP].options}")

    def renew(self):
        try:
            x_id = random.randrange(1, 1000000)
            req = IP(src=self.ip, dst=self.server_ip) / UDP(sport=68, dport=67) / BOOTP(
                op="BOOTREQUEST", xid=x_id, chaddr=self.mac_str) / DHCP(options=self.req_options)
            t1 = time.time()
            self.log.debug(f"Doing renew at {t1} - renew time: {self.renew_time}")
            resp = sr1(req, iface=self.iface, timeout=2.5, verbose=0)
            t2 = time.time()
            self._parse_renewal_time(resp, t2)
            self.log.debug(f"Renew succeeded in {t2-t1} - next renew time: {self.renew_time}")
            return t2-t1
        except Exception as e:
            self.log.debug(f"Renew failed: {str(e)}")
            return e

