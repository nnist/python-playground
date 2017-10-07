#!/usr/bin/env python3

# TODO Do not throw error when Ctrl-C is pressed

import pyshark
import time
import sys
import os

def main(argv):
    print('Starting capture.')
    #capture = pyshark.LiveCapture(interface='enp2s0', bpf_filter='tcp port 80')
    capture = pyshark.LiveCapture(interface='enp2s0')

    packet_count = 0
    sources = []

    # Capture packets
    for packet in capture.sniff_continuously(packet_count=1000):
        #print('Just arrived:', packet)

        src_ip = '?'
        dst_ip = '?'
        packet_type = '?'

        if 'ARP' in packet:
            packet_type = 'ARP'
            src_ip = packet.arp.src_proto_ipv4
            dst_ip = packet.arp.dst_proto_ipv4

        if 'IP' in packet:
            packet_count += 1
            packet_type = 'IP'
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
            
            #print(packet.ip.field_names)
            if packet.ip.src not in sources:
                sources.append(packet.ip.src)

        if 'UDP' in packet:
            packet_type = 'UDP'
            src_port = packet.udp.srcport
            dst_port = packet.udp.dstport

        if 'OPENVPN' in packet:
            packet_type = 'OPENVPN'
        
        print('{num} {time} {src} -> {dst} {pkt_type}'.format(num=packet_count,
            time=time.clock(), src=src_ip, dst=dst_ip,
            pkt_type=packet_type))

    print('-------------------------------------')
    count = str(packet_count)
    cap_time = str(time.clock())
    print('Captured {} packets in {} minutes.'.format(count, cap_time))
    print(sources)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
