from unittest import TestCase
from massdhclient import DHCPClient, ClientHerd
from subprocess import call
import sys
import logging

logging.basicConfig(level=logging.DEBUG)


class TestClientHerd(TestCase):
    def setUp(self) -> None:
        self.iface = "en7"
        exitcode = call(["ifconfig", self.iface, "promisc"], stdout=None, stderr=None, shell=False)
        if exitcode:
            print(f"No such device: {self.iface}")
            # sys.exit()

    def test_small_herd(self):

        herd = ClientHerd(self.iface, 5)
        herd.start(1)
        print(f"Retrieved an IP in {self.client.discover()} seconds: {self.client.ip}..")
        print(f"Renewing {self.client.ip}..")
        import time
        time.sleep(2)
        print(f"renew done in {self.client.renew()} seconds")
        print("Done")

