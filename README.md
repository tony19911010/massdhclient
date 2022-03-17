# Introduction 
Mass DHCP Client emulator is a tool, designed to emulate thousands of dhcp clients on an interface, 
in order to measure load, and meantime from DISCOVER to DHCPACK

# Installation
```
pip install massdhclient
```

# Usage
```
./massdhclient.py -n 1000 --mac 12:34:56:00:00:00 -i 0.1
```
* Will start 1000 clients using artifical mac addresses starting from the specified mac address.
* Once half the leasetime is up, each client will attempt to renew its lease, like a good dhcp client.
* Each new client will be started with an interval of 0.1 seconds
* will periodically update on the average time a discover or renew process is taking
# Contribute
Feel free