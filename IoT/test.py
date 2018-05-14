from scapy.all import *


pcap = rdpcap("/home/luigi/Downloads/milight-remote-startup-and-on-off-just-ip.pcap")

for p in pcap[100:]:
    if 'TCP' in p:
        #print str(p['TCP'].payload)
        #print p['IP'].src + "--> " + p['IP'].dst
        #if p['IP'].src == '192.168.101.247':
        #if p['IP'].src == '34.242.121.115':
        print str(p.time) + " " + p['IP'].src + "      " + str(p['TCP'].payload).encode('hex')


# 1 on
# 2 off
