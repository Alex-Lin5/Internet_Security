#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/udp.h>
#include <linux/icmp.h>
#include <linux/if_ether.h>
#include <linux/inet.h>

#define VM_IP "10.9.0.1"

static struct nf_hook_ops hook_lin, hook_lout, hook_prert, hook_for, hook_pstrt,
   hook_blkp2VM, hook_blktl2VM; 

unsigned int printInfo(void *priv, struct sk_buff *skb,
                 const struct nf_hook_state *state)
{
   struct iphdr *iph;
   char *hook;
   char *protocol;

   switch (state->hook){
     case NF_INET_LOCAL_IN:     hook = "LOCAL_IN";     break; 
     case NF_INET_LOCAL_OUT:    hook = "LOCAL_OUT";    break; 
     case NF_INET_PRE_ROUTING:  hook = "PRE_ROUTING";  break; 
     case NF_INET_POST_ROUTING: hook = "POST_ROUTING"; break; 
     case NF_INET_FORWARD:      hook = "FORWARD";      break; 
     default:                   hook = "IMPOSSIBLE";   break;
   }
   printk(KERN_INFO "*** %s\n", hook); // Print out the hook info

   iph = ip_hdr(skb);
   switch (iph->protocol){
     case IPPROTO_UDP:  protocol = "UDP";   break;
     case IPPROTO_TCP:  protocol = "TCP";   break;
     case IPPROTO_ICMP: protocol = "ICMP";  break;
     default:           protocol = "OTHER"; break;

   }
   // Print out the IP addresses and protocol
   printk(KERN_INFO "    %pI4  --> %pI4 (%s)\n", 
                    &(iph->saddr), &(iph->daddr), protocol);

   return NF_ACCEPT;
}

unsigned int blockICMP(void *priv, struct sk_buff *skb,
                       const struct nf_hook_state *state)
{
   struct iphdr *iph;
   struct icmphdr *icmph;

   char ip[16] = VM_IP;
   u32  ip_addr;

   if (!skb) return NF_ACCEPT;

   iph = ip_hdr(skb);
   // Convert the IPv4 address from dotted decimal to 32-bit binary
   in4_pton(ip, -1, (u8 *)&ip_addr, '\0', NULL);

   if (iph->protocol == IPPROTO_ICMP) {
       icmph = icmp_hdr(skb);
       if (iph->daddr == ip_addr){
            printk(KERN_WARNING "*** Dropping %pI4 (ICMP)\n", &(iph->daddr));
            return NF_DROP;
        }
   }
   return NF_ACCEPT;
}

unsigned int blockTCP(void *priv, struct sk_buff *skb,
                       const struct nf_hook_state *state)
{
   struct iphdr *iph;
   struct tcphdr *tcph;

   u16  port   = 23;
   char ip[16] = VM_IP;
   u32  ip_addr;

   if (!skb) return NF_ACCEPT;

   iph = ip_hdr(skb);
   // Convert the IPv4 address from dotted decimal to 32-bit binary
   in4_pton(ip, -1, (u8 *)&ip_addr, '\0', NULL);

   if (iph->protocol == IPPROTO_TCP) {
       tcph = tcp_hdr(skb);
       if (iph->daddr == ip_addr && ntohs(tcph->dest) == port){
            printk(KERN_WARNING "*** Dropping %pI4 (TCP-telnet), port %d\n", &(iph->daddr), port);
            return NF_DROP;
        }
   }
   return NF_ACCEPT;
}

int registerFilter(void) {
   printk(KERN_INFO "Registering filters.\n");

   hook_lout.hook = printInfo;
   hook_lout.hooknum = NF_INET_LOCAL_OUT;
   hook_lout.pf = PF_INET;
   hook_lout.priority = NF_IP_PRI_FIRST;
   nf_register_net_hook(&init_net, &hook_lout);

   hook_pstrt.hook = printInfo;
   hook_pstrt.hooknum = NF_INET_POST_ROUTING;
   hook_pstrt.pf = PF_INET;
   hook_pstrt.priority = NF_IP_PRI_FIRST;
   nf_register_net_hook(&init_net, &hook_pstrt);

   hook_lin.hook = printInfo;
   hook_lin.hooknum = NF_INET_LOCAL_IN;
   hook_lin.pf = PF_INET;
   hook_lin.priority = NF_IP_PRI_FIRST;
   nf_register_net_hook(&init_net, &hook_lin);

   hook_for.hook = printInfo;
   hook_for.hooknum = NF_INET_FORWARD;
   hook_for.pf = PF_INET;
   hook_for.priority = NF_IP_PRI_FIRST;
   nf_register_net_hook(&init_net, &hook_for);

   hook_prert.hook = printInfo;
   hook_prert.hooknum = NF_INET_PRE_ROUTING;
   hook_prert.pf = PF_INET;
   hook_prert.priority = NF_IP_PRI_FIRST;
   nf_register_net_hook(&init_net, &hook_prert);

   hook_blkp2VM.hook = blockICMP;
   hook_blkp2VM.hooknum = NF_INET_LOCAL_IN;
   hook_blkp2VM.pf = PF_INET;
   hook_blkp2VM.priority = NF_IP_PRI_FIRST;
   nf_register_net_hook(&init_net, &hook_blkp2VM);

   hook_blktl2VM.hook = blockTCP;
   hook_blktl2VM.hooknum = NF_INET_LOCAL_IN;
   hook_blktl2VM.pf = PF_INET;
   hook_blktl2VM.priority = NF_IP_PRI_FIRST;
   nf_register_net_hook(&init_net, &hook_blktl2VM);

   return 0;
}

void removeFilter(void) {
   printk(KERN_INFO "The filters are being removed.\n");
   nf_unregister_net_hook(&init_net, &hook_lout);
   nf_unregister_net_hook(&init_net, &hook_pstrt);
   nf_unregister_net_hook(&init_net, &hook_lin);
   nf_unregister_net_hook(&init_net, &hook_prert);
   nf_unregister_net_hook(&init_net, &hook_for);
   nf_unregister_net_hook(&init_net, &hook_blkp2VM);
   nf_unregister_net_hook(&init_net, &hook_blktl2VM);
}

module_init(registerFilter);
module_exit(removeFilter);

MODULE_LICENSE("GPL");

