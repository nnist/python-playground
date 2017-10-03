#!/usr/bin/env python
from scapy.all import *
 
def pkt_callback(pkt):
        #pkt.show()
        print(pkt.src)
        print(pkt.dst)
        pass
       
sniff(iface="enp2s0", prn=pkt_callback, filter="ip", store=0)
