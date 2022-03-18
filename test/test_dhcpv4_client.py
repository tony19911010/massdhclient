from unittest import TestCase
from massdhclient import DHCPClient
from subprocess import call
import sys


class TestDHCPClient(TestCase):
    def setUp(self) -> None:
        self.iface = "en8"
        exitcode = call(["ifconfig", self.iface, "promisc"], stdout=None, stderr=None, shell=False)
        if exitcode:
            print(f"No such device: {self.iface}")
            #sys.exit()
        self.client = DHCPClient(self.iface)

    def test_discover(self):
        print(f"Retrieved an IP in {self.client.discover()} seconds: {self.client.ip}..")
        print(f"Renewing {self.client.ip}..")
        import time
        time.sleep(2)
        print(f"renew done in {self.client.renew()} seconds")
        print("Done")



    def test_renew(self):
        self.fail()
