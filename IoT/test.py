from scapy.all import *


pcap = rdpcap("/home/luigi/Downloads/milight-remote-startup-and-on-off-just-ip.pcap")
pcap = rdpcap("captures/c")

for p in pcap:
    if 'TCP' in p:
        payload = p['TCP'].payload
        if not payload: continue

        #if p['IP'].src == '192.168.101.247':
        if p['IP'].src == '34.242.121.115':
            print "%-15s %s          %s" % (str(p.time),p['IP'].src,str(payload).encode('hex'))


# 1 on
# 2 off
