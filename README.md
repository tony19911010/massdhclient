# Introduction 
Mass DHCP Client emulator is a tool, designed to emulate thousands of dhcp clients on an interface, 
in order to measure load, and meantime from DISCOVER to DHCPACK

# Installation
```
pip install massdhclient
```

# Usage
```
massdhcpclient.py -h
usage: massdhcpclient.py [-h] [-d] [-p INTERFACE] [-i INTERVAL] [-l LOGFILE] [-c CLIENTS] [-m BASE_MAC] [-n HOST_PREFIX]

Mass DHCP Client simulator

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug
  -p INTERFACE, --interface INTERFACE
                        Interface on which to issue requests
  -i INTERVAL, --interval INTERVAL
                        Interval between starting next client
  -l LOGFILE, --logfile LOGFILE
                        Direct logs to specified file
  -c CLIENTS, --clients CLIENTS
                        Number of clients to spawn
  -m BASE_MAC, --mac BASE_MAC
                        Initial MAC address of first client (is incremented for each additional client)
  -n HOST_PREFIX, --hostname HOST_PREFIX
                        Hostname prefix of the clients - will be postfixed with client number (6 leading zeroes)

massdhcpclient.py -c 1000 --mac 12:34:56:00:00:00 -i 0.1
```
* Will start 1000 clients using artifical mac addresses starting from the specified mac address.
* Once half the leasetime is up, each client will attempt to renew its lease, like a good dhcp client.
* Each new client will be started with an interval of 0.1 seconds
* will periodically update on the average time a discover or renew process is taking
# Contribute
Feel free