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
   
    src_ip = pkt.sprintf("%IP.src%")
    src_tcp_port = pkt.sprintf("%TCP.sport%")
    
    dst_ip = pkt.sprintf("%IP.dst%")
    dst_tcp_port = pkt.sprintf("%TCP.dport%")

    tcp_flags = pkt.sprintf("%2s,TCP.flags%")
    tcp_payload = pkt.sprintf("%TCP.payload%")

    ip_id = pkt.sprintf("%IP.id%")

    raw = pkt.sprintf("%Raw.load%") 
    print(raw)

    #print(src_ip, src_tcp_port, "->", dst_ip, dst_tcp_port, "\n", tcp_flags, tcp_payload)
    #pkt.show()
    #print(dir(pkt))
    #print(pkt.src)
    #print(pkt.summary)
    #print(pkt.dst)
    #print(tabulate(msg))
    #return pkt.sprintf(str(msg))
    #pass

sniff(iface="enp2s0", prn=pkt_callback, store=0)
#sniff(iface="enp2s0", prn=pkt_callback, filter="", store=0)
