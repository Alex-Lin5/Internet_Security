#!/usr/bin/env python3
from scapy.all import IP, DNS, UDP, send, DNSQR

DNS_SERVER = '10.9.0.53'
ATK_NS = '10.9.0.153'
USER_IP = '10.9.0.5'

Qdsec = DNSQR(qname='abcde.example.com')
dns = DNS(id=0xAAAA, qr=0, qdcount=1, ancount=0, nscount=0, arcount=0, qd=Qdsec)
ip = IP(dst=DNS_SERVER, src=USER_IP)
udp = UDP(dport=53, sport=12345, chksum=0)
request = ip/udp/dns
send(request)
print(request.summary())
with open('ip_req.bin', 'wb') as f:
  f.write(bytes(request))
