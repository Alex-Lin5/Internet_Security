#!/usr/bin/env python3
from scapy.all import IP, socket
import os, fcntl, struct, select

IP_A = "0.0.0.0"
ROUTER = "192.168.60.11"
PORT = 9090
TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000

# create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_A, PORT))

# Create the tun interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'lin%d', IFF_TUN | IFF_NO_PI)
ifname_bytes  = fcntl.ioctl(tun, TUNSETIFF, ifr)
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
os.system("ip addr add 192.168.53.77/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

print("Server program running...")
print("Interface Name: {}".format(ifname))
print('tun: ', tun)

while True:
  # # single direction communication, only receive packets from client via socket
  # data, (ip, port) = sock.recvfrom(2048)
  # print("{}:{} --> {}:{}".format(ip, port, IP_A, PORT))
  # pkt = IP(data)
  # print(" Inside: {} --> {}".format(pkt.src, pkt.dst))
  # os.write(tun, data)
  # print('----------------')
  
  # two-way communication
  fds = [sock, tun]
  ready, _, _ = select.select(fds, [], [])
  for fd in ready:
    if fd is sock:
      data, (ip, port) = sock.recvfrom(2048)
      os.write(tun, data)
      pkt = IP(data)
      print("From socket <==: {} --> {}".format(pkt.src, pkt.dst))
      print(pkt.summary())
    if fd is tun:
      packet = os.read(tun, 2048)
      sock.sendto(packet, (ip, port))
      pkt = IP(packet)
      print("From tun    ==>: {} --> {}".format(pkt.src, pkt.dst))
      print(pkt.summary())
