from scapy.all import rdpcap
from scapy.layers.inet import TCP, UDP
from scapy.layers.dns import DNS
from scapy.layers.ntp import NTP
from collections import defaultdict

packets = rdpcap("NonVPN-PCAPs-01/facebookchat3.pcapng")

layer_counts = defaultdict(int)

for pkt in packets:
    for layer in [TCP, UDP, DNS, NTP]:
        if pkt.haslayer(layer):
            layer_counts[layer.__name__] += 1

print("\n=== Zliczanie warstw ===")
for layer, count in layer_counts.items():
    print(f"  {layer}: {count} pakietów")
