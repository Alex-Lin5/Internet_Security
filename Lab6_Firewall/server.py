import os

# restore table configuration to default setting
os.system("iptables -t filter -F")
os.system("iptables -t filter -P OUTPUT ACCEPT")
os.system("iptables -t filter -P INPUT ACCEPT")
os.system("iptables -t filter -P FORWARD ACCEPT")

# Task 2C
# add rules for default table filter in router machine
# eth0 is 10.9.0.11
# eth1 is 192.168.60.11
# os.system("iptables -t filter -A FORWARD -d 192.168.60.5 -p tcp --dport 23 -j ACCEPT")
# os.system("iptables -t filter -A FORWARD -s 192.168.60.5 -p tcp --sport 23 -j ACCEPT")
# os.system("iptables -t filter -P INPUT DROP")
# os.system("iptables -t filter -P FORWARD DROP")
# # os.system("iptables -t filter -A FORWARD -d 192.168.60.5 -i eth0 -p tcp --dport 23 -j ACCEPT")
# # os.system("iptables -t filter -A FORWARD -s 192.168.60.5 -o eth1 -p tcp --sport 23 -j ACCEPT")

# Task 3B
# add rules for default table filter in router machine
os.system("iptables -t filter -P INPUT DROP")
os.system("iptables -t filter -P FORWARD DROP")
os.system("iptables -t filter -A FORWARD -p tcp -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT")
os.system("iptables -t filter -A FORWARD -i eth0 -p tcp --dport 23 -d 192.168.60.5 --syn -m conntrack --ctstate NEW -j ACCEPT")
os.system("iptables -t filter -A FORWARD -o eth0 -p tcp --dport 23 --syn -m conntrack --ctstate NEW -j ACCEPT")
os.system("iptables -t filter -A FORWARD -p icmp -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT")
os.system("iptables -t filter -A FORWARD -o eth0 -p icmp --icmp-type echo-request -m conntrack --ctstate NEW -j ACCEPT")
os.system("iptables -t filter -A FORWARD -p udp -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT")
os.system("iptables -t filter -A FORWARD -o eth0 -p udp --dport 9090 -m conntrack --ctstate NEW -j ACCEPT")

# print out iptable table filter rules and connection track information
os.system("iptables -t filter -L -n --line-numbers")
os.system("conntrack -L")
print("\n\n\n")
