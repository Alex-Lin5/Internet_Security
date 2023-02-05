from scapy.all import *

fndst = '8.8.8.8'
# VMsrc = '10.9.0.1'
VMsrc = '10.0.2.4'
ip = IP(src=VMsrc, dst=fndst)
icmp = ICMP()
dstls = [VMsrc]
TTL = 1
while True:
    ip.ttl = TTL
    res = sr1(ip/icmp, verbose=0)    
    dstls.append(res.src)
    print(TTL, '...')
    res.show()
    TTL += 1
    if(TTL >= 15): break
    if(res.dst == fndst): break

dstls.append(fndst)    
print(dstls)  
