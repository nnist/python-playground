#!/usr/bin/env python3

# TODO Do not throw error when Ctrl-C is pressed

import pyshark
import time
import sys
import os
import curses

connections = []

def find_connection(src_ip, dst_ip):
    # Find connection in a list of connections, return index or None
    for i in range(len(connections)):
        connection_src_ip = connections[i][0]
        connection_dst_ip = connections[i][1]
        if connection_src_ip == src_ip and connection_dst_ip == dst_ip:
            return i
    return None

def main(argv):
    stdscr = curses.initscr()
    stdscr.timeout(1)
    stdscr.nodelay(True)
    curses.noecho()
    curses.cbreak()
    #begin_x = 20
    #begin_y = 7
    #height = 5
    #width = 40
    #win = curses.newwin(height, width, begin_y, begin_x)
    stdscr.refresh()
    #capture = pyshark.LiveCapture(interface='enp2s0', bpf_filter='tcp port 80')
    capture = pyshark.LiveCapture(interface='enp2s0')

    packet_count = 0

    # Capture packets until q is pressed
    for packet in capture.sniff_continuously():
        c = stdscr.getch()
        if c == ord('q'):
            curses.nocbreak()
            curses.echo()
            curses.endwin()
            sys.exit(0)
            #break
        
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

        if 'UDP' in packet:
            packet_type = 'UDP'
            src_port = packet.udp.srcport
            dst_port = packet.udp.dstport

        if 'OPENVPN' in packet:
            packet_type = 'OPENVPN'
       
        # Find connection in list. Add if not found. Increment if found.
        connection_index = find_connection(src_ip, dst_ip) 
        if connection_index is None:
            connections.append((src_ip, dst_ip, 0))
        else:
            # TODO increment by one
            connection = (connections[i][0], connections[i][1], connections[i][2] + 1)
            connections[i] = connection

        # TODO Hide cursor
        stdscr.addstr(0, 0, "{} packets captured".format(str(packet_count)), curses.A_BOLD) 
        
        for i in range(len(connections)):
            connection = connections[i]
            src = connection[0]
            dst = connection[1]
            cnt = connection[2]
            try:
                stdscr.addstr(i+1, 0, "[{}] {} -> {}".format(cnt, src, dst))
            except:
                #print('uh oh')
                pass

        stdscr.refresh()
    
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    sys.exit(0)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        try:
            curses.nocbreak()
            curses.echo()
            curses.endwin()
            sys.exit(0)
        except SystemExit:
            os._exit(0)
