#!/usr/bin/env python3
from scapy.all import IP, socket
import os, fcntl, struct, select

IP_A = "0.0.0.0"
Client_Eth0 = '10.9.0.12'
Server_Eth0 = '10.9.0.11'
UserNetwork = '192.168.50.0/24'
Server_Port = 9090
TUNIP = '192.168.53.77'
TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000

# create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_A, Server_Port))

# Create the tun interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'lin%d', IFF_TUN | IFF_NO_PI)
ifname_bytes  = fcntl.ioctl(tun, TUNSETIFF, ifr)
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
os.system("ip addr add {}/24 dev {}".format(TUNIP, ifname)) # add network mask to let TUN interface display on routing table
os.system("ip link set dev {} up".format(ifname))
# add routing direction, route network on the other side to TUN interface
os.system("ip route add {} dev {}".format(UserNetwork, ifname))

print("Server program running...")
print("Interface Name: {}".format(ifname))
print('tun: ', tun)

while True:
  # # single direction communication, only receive packets from client via socket
  # data, (ip, port) = sock.recvfrom(2048)
  # print("{}:{} --> {}:{}".format(ip, port, IP_A, Server_Port))
  # pkt = IP(data)
  # print(" Inside: {} --> {}".format(pkt.src, pkt.dst))
  # os.write(tun, data)
  # print('----------------')
  
  # two-way communication
  fds = [sock, tun]
  ready, _, _ = select.select(fds, [], [])
  for fd in ready:
    if fd is sock:
      data, (ip, Client_port) = sock.recvfrom(2048) # sock will receive first packet from user
      os.write(tun, data)
      pkt = IP(data)
      print("From socket <==: {} --> {}".format(pkt.src, pkt.dst))
      print(pkt.summary())
    if fd is tun:
      packet = os.read(tun, 2048)
      pkt = IP(packet)
      sock.sendto(packet, (Client_Eth0, Client_port)) # (ip, Client_port) only availbe when client initiate first packet
      print("From tun    ==>: {} --> {}".format(pkt.src, pkt.dst))
      print(pkt.summary())
