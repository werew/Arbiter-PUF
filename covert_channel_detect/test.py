from scapy.all import *


pcap = rdpcap("sample2.pcapng")

for p in pcap:
    if 'TCP' in p:
        sport = p['TCP'].sport
        dport = p['TCP'].dport
        print str(sport)+" "+str(dport)+" "+str(p['TCP'].flags)

