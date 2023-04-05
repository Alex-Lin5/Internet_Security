import os

# restore table configuration to default setting
os.system("iptables -F")
os.system("iptables -P OUTPUT ACCEPT")
os.system("iptables -P INPUT ACCEPT")
os.system("iptables -P FORWARD ACCEPT")

# add rules for default table filter in router machine
os.system("iptables -t filter -A INPUT -d 192.168.60.11 -p icmp --icmp-type echo-request -j ACCEPT")
os.system("iptables -t filter -P INPUT DROP")
os.system("iptables -t filter -A FORWARD -s 192.168.60.0/24 -p icmp --icmp-type echo-request -j ACCEPT")
os.system("iptables -t filter -A FORWARD -d 192.168.60.0/24 -p icmp --icmp-type echo-reply -j ACCEPT")
os.system("iptables -t filter -P FORWARD DROP")
# eth0 is 10.9.0.11
# eth1 is 192.168.60.11
# os.system("iptables -t filter -A FORWARD -o eth0 -p icmp --icmp-type echo-request -j ACCEPT")
# os.system("iptables -t filter -A FORWARD -i eth1 -p icmp --icmp-type echo-reply -j ACCEPT")
# os.system("iptables -t filter -A FORWARD -o eth0@if21 -p icmp --icmp-type echo-request -j ACCEPT")
# os.system("iptables -t filter -A FORWARD -i eth1@if19 -p icmp --icmp-type echo-reply -j ACCEPT")
# print out iptable table filter rules
os.system("iptables -t filter -L -n --line-numbers")

# Delete rule 2 in INPUT chain of filter table
# iptables -t filter -D INPUT 2
