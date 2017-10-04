# https://scapy.readthedocs.io/en/latest/usage.html#identifying-rogue-dhcp-servers-on-your-lan

# send a DHCP discover request and analyze the replies
conf.checkIPaddr = False
fam,hw = get_if_raw_hwaddr(conf.iface)
dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=hw)/DHCP(options=[("message-type","discover"),"end"])
ans, unans = srp(dhcp_discover, multi=True)

# In this case we got 2 replies, so there were two active DHCP servers on the test network:
ans.summary()

# We are only interested in the MAC and IP addresses of the replies:
for p in ans: print p[1][Ether].src, p[1][IP].src
