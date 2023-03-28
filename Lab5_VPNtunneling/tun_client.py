#!/usr/bin/env python3

import fcntl, select, struct, os
from scapy.all import IP, ICMP, UDP, socket

H1 = '192.168.60.5'
SERVER_PORT = 9090
TUNIP = '192.168.53.99'
Client_Eth0 = '10.9.0.12'
Server_Eth0 = '10.9.0.11'
HostNetwork = '192.168.60.0/24'
TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000

# Create the tun interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'lin%d', IFF_TUN | IFF_NO_PI)
ifname_bytes  = fcntl.ioctl(tun, TUNSETIFF, ifr)

# Get the interface name
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Client program running...")
print("Interface Name: {}".format(ifname))
print('tun: ', tun)
os.system("ip addr add {}/24 dev {}".format(TUNIP, ifname)) # add network mask to let TUN interface display on routing table
os.system("ip link set dev {} up".format(ifname))

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# add routing direction, route network on the other side to TUN interface
os.system("ip route add {} dev {}".format(HostNetwork, ifname))

# Hold the tunnel running
while True:
  # two-way communication
  fds = [sock, tun]
  ready, _, _ = select.select(fds, [], [])
  for fd in ready:
    if fd is sock:
      data, (ip, port) = sock.recvfrom(2048)
      os.write(tun, data)
      pkt = IP(data)
      print('From SOCK <-, ', pkt.summary())
    if fd is tun:
      packet = os.read(tun, 2048)
      pkt = IP(packet)
      sock.sendto(packet, (Server_Eth0, SERVER_PORT))
      print('From TUN  ->, ', pkt.summary())
  
  # ospacket = os.read(tun, 2048)
  # # Get a packet from the tun interface, READ 
  # if ospacket:
  #   # print('Raw packet:', ospacket)
  #   # b'E\x00\x00T|\xc9@\x00@\x01\xc4\x89\xc0\xa8<\x00\xc0\xa8<\x05\x08\x00\xf8.\x02\x1b\x00\x02I\x08\x06d\x00\x00\x00\x00\xe7t\x08\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'
  #   pkt = IP(ospacket)
  #   print('read: ', pkt.summary())		
  #   # Send the packet via the tunnel
  #   sock.sendto(ospacket, (Server_Eth0, SERVER_PORT))

  #   # Send out a spoof packet using the tun interface, WRITE       
  #   if False: pass
  #   # elif(ICMP in pkt and pkt[ICMP].type == 8):
  #   #   newip = IP(src=pkt[IP].dst, dst=pkt[IP].src)
  #   #   print('packet in ICMP protocol.')
  #   #   echoReply = ICMP(type=0, code=0)
  #   #   echoReq = ICMP(type=8, code=0)
  #   #   # newip[IP].remove_payload()      
  #   #   newpkt = newip/echoReply
  #   #   os.write(tun, bytes(newpkt))   
  #   #   print('write:', newpkt.summary())
  #   elif(UDP in pkt):
  #     print('packet in UDP protocol.')

  #   # spoof an arbitary packet
  #   # newpkt = b'E\x00\x08T|\xc9@\x00@\x01\xc4'
  #   # os.write(tun, bytes(newpkt))   
  #   # ospacket = os.read(tun, 2048)
  #   # print('spoof newpkt,', newpkt)
  #   # print('read raw,', ospacket) 
  #   print('---------------')

