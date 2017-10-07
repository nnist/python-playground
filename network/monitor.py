#!/usr/bin/env python
from scapy.all import *
from tabulate import tabulate
 
def pkt_callback(pkt):
    # TODO add blacklist
    msg = []
    msg.append(("Packet name", pkt.name))
    msg.append(("Sent time", pkt.sent_time))
    msg.append(("Time", pkt.time))
    msg.append(("Fields", pkt.fields))
    msg.append(("Type", pkt.type))
    
    #pkt.show()
    #print(dir(pkt))
    #print(pkt.src)
    #print(pkt.summary)
    #print(pkt.dst)
    print(tabulate(msg))
    
    #return pkt.sprintf(str(msg))
    pass

sniff(iface="enp2s0", prn=pkt_callback, store=0)
#sniff(iface="enp2s0", prn=pkt_callback, filter="", store=0)
