from scapy.all import *

ip1 = IP()
ip1.dst = '10.9.0.6'
ip1.src = '10.9.0.5'
icmp1 = ICMP()
pkt = ip1/icmp1
send(pkt)
# print("ls(pkt)..........")
# ls(pkt)
pkt.show()
