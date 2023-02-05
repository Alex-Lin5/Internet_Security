from scapy.all import *

def spoof_pkt(pkt):
    if ICMP in pkt and pkt[ICMP].type == 8:
    	print("Original packet...")
    	pkt.show()
    	ip = IP(src=pkt[IP].dst, dst=pkt[IP].src, ihl=pkt[IP].ihl, flags=pkt[IP].flags)
    	icmp = ICMP(type=0, id=pkt[ICMP].id, seq=pkt[ICMP].seq, chksum=pkt[ICMP].chksum)
    	data = pkt[Raw].load
    	print("Spoofed packet...")
    	newpkt = ip/icmp/data
    	send(newpkt, verbose=0)
    	newpkt.show()
    	print("*************")

pkt = sniff(iface='br-f659e2f7cd2a', filter='icmp and src host 10.9.0.5', prn=spoof_pkt)
