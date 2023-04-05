import os

# restore table configuration to default setting
os.system("iptables -t nat -F")
os.system("iptables -t nat -P OUTPUT ACCEPT")
os.system("iptables -t nat -P INPUT ACCEPT")
os.system("iptables -t nat -P FORWARD ACCEPT")

# configure load balancing
os.system("iptables -t nat -A PREROUTING -p udp --dport 8080 \
  -m statistic --mode nth --every 3 --packet 0 \
  -j DNAT --to-destination 192.168.60.5:8080")
os.system("iptables -t nat -A PREROUTING -p udp --dport 8080 \
  -m statistic --mode nth --every 3 --packet 1 \
  -j DNAT --to-destination 192.168.60.6:8080")
os.system("iptables -t nat -A PREROUTING -p udp --dport 8080 \
  -m statistic --mode nth --every 3 --packet 2 \
  -j DNAT --to-destination 192.168.60.7:8080")


# print out iptable packets statistic mode and rule
os.system("iptables -t nat -L -n --line-numbers")

# feeding UDP packets 
# os.system("nc -lu 8080")
# idx = 0
# while idx < 100:      
#   os.system("echo " + idx + ".\n > /dev/udp/192.168.60.11/8080")
#   idx+=1
