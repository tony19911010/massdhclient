from netaddr import EUI, mac_unix_expanded
from .dhcpv4_client import DHCPClient
import time
from concurrent.futures import ThreadPoolExecutor, Future
from queue import Queue


class ClientHerd:
    def __init__(self, iface, size, base_mac="00:00:5e:fa:00:00", hostname_prefix="C00"):
        self.clients = {}
        mac = EUI(base_mac, dialect=mac_unix_expanded)
        self.avg = None

        for x in range(size):
            c = DHCPClient(iface, str(mac), f"{hostname_prefix}{x:06}")
            self.clients[c.mac] = c
            mac.value += 1

    def start(self, interval=0.5):
        # pool sized for to run needed parallel instances for interval when each session is 10 seconds
        pool = ThreadPoolExecutor(int(10/interval)+1)
        queue = []
        for mac, c in self.clients.items():
            queue.append((mac, pool.submit(c.discover)))
            time.sleep(interval)
        while queue:
            mac, fut = queue.pop(0)
            res = fut.result()
            if isinstance(res, Exception):
                self.clients[mac].log.warning(f"Retrying discover immediately: {str(res)}")
                queue.append((mac, pool.submit(self.clients[mac].discover)))
            else:
                self.capture_stats(res)
        pool.shutdown()

    def renew(self):
        pool = ThreadPoolExecutor(20)
        queue = []
        for mac, c in self.clients.items():
            if c.renew_time and c.renew_time < time.time():
                queue.append((mac, pool.submit(self.clients[mac].renew)))
        renewed = len(queue)
        while queue:
            mac, fut = queue.pop(0)
            res = fut.result()
            if isinstance(res, Exception):
                self.clients[mac].log.warning(f"Retrying renew immediately: {str(res)}")
                queue.append((mac, pool.submit(self.clients[mac].renew)))
            else:
                self.capture_stats(res)
        pool.shutdown()
        return renewed

    def capture_stats(self, value):
        if not self.avg:
            self.avg = value
        else:
            self.avg = self.avg * 0.97 + 0.03*value
