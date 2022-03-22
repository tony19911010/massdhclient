#!/usr/bin/env python3

import logging
import argparse
import time


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='Mass DHCP Client simulator')
    parser.add_argument('-d', '--debug', dest='debug', action='store_const', default=False, const=True)
    parser.add_argument('-p', '--interface', dest='interface', default='eth0', help="Interface on which to issue requests")
    parser.add_argument('-i', '--interval', dest='interval', type=float, default=0.5, help="Interval between starting next client")
    parser.add_argument('-l', '--logfile', dest='logfile', default=None, help="Direct logs to specified file")
    parser.add_argument('-c', '--clients', dest='clients', type=int, default=10, help="Number of clients to spawn")
    parser.add_argument('-m', '--mac', dest='base_mac', default="00:00:5e:fa:00:01",
                        help="Initial MAC address of first client (is incremented for each additional client)")
    parser.add_argument('-n', '--hostname', dest='host_prefix', default="C",
                        help="Hostname prefix of the clients - will be postfixed with client number (6 leading zeroes)")

    args = parser.parse_args()

    root_logger = logging.getLogger()
    log_format = "%(name)-55s %(levelname)-8s %(message)s"
    log_stream = logging.StreamHandler()
    log_stream.setFormatter(logging.Formatter("%(asctime)s: " + log_format, '%H:%M:%S'))
    root_logger.setLevel(logging.INFO if args.debug else logging.WARNING)
    log = logging.getLogger('massdhclient')
    log.setLevel(logging.DEBUG if args.debug else logging.INFO)
    root_logger.addHandler(log_stream)

    if args.logfile:
        logfile = logging.FileHandler(args.logfile)
    root_logger.info(f"Starting up a herd of {args.clients} clients on {args.interface} - one every {args.clients} seconds")
    import subprocess
    import sys

    exitcode = subprocess.call(["ifconfig", args.interface, "promisc"], stdout=None, stderr=None, shell=False)
    if exitcode != 0:
        print(f"Unable to make {args.interface} promiscuous :/")
        sys.exit()
    import massdhclient
    herd = massdhclient.ClientHerd(args.interface, args.clients, args.base_mac, args.host_prefix)
    herd.start(args.interval)
    log.info(f"All clients have now acquired addresses - avg time is {herd.avg} s/Lease with {herd.retries} retries")
    log.info("Proceeding to renew addresses as needed - CTRL-C to exit")
    while True:
        time.sleep(10)
        renewed = herd.renew()
        if renewed:
            log.info(f"Renewed {renewed} clients - avg time is now {herd.avg} s/Lease")





