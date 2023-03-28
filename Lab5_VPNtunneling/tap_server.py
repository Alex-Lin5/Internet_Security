import fcntl, struct, os, select
from scapy.all import ARP, Ether, socket

SERVER_PORT = 9090
TAPIP = '192.168.53.77'
Client_Eth0 = '10.9.0.12'
Server_Eth0 = '10.9.0.11'
UserNetwork = '192.168.50.0/24'
TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000

tap = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack("16sH", b"tap%d", IFF_TAP | IFF_NO_PI)
ifname_bytes = fcntl.ioctl(tap, TUNSETIFF, ifr)
ifname = ifname_bytes.decode("UTF-8")[:16].strip("\x00")

# Setup TAP interface
os.system('ip link set dev {} up'.format(ifname))

# Bridging, use a bridge to connect tap0 and private network interface
br = 'br0'
os.system('ip link add name {} type bridge'.format(br))
os.system('ip link set {} master {}'.format('eth1', br))
os.system('ip link set {} master {}'.format(ifname, br))
os.system('ip link set dev {} up'.format(br))

print("Server program running...")
print("Interface Name: {}".format(ifname))
print('tap: ', tap)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fds = [sock, tap]
while True:
  # two-way communication
  ready, _, _ = select.select(fds, [], [])
  for fd in ready:
    if fd is sock:
      data, (ip, port) = sock.recvfrom(2048)
      os.write(tap, data)
      pkt = Ether(data)
      print('From SOCK <-, ', pkt.summary())
    if fd is tap:
      packet = os.read(tap, 2048)
      pkt = Ether(packet)
      sock.sendto(packet, (Client_Eth0, SERVER_PORT))
      print('From TUN  ->, ', pkt.summary())
