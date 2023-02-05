from scapy.all import *

def print_pkt(pkt):
    pkt.show()
    # pkt.summary()
    print("*************")
pkt = sniff(iface='br-f659e2f7cd2a', filter='net 10.9.0.0/24 ', prn=print_pkt)
