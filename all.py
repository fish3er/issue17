from matplotlib import pyplot as plt
from scapy.all import rdpcap
from scapy.layers.inet import TCP, UDP
from scapy.layers.dns import DNS
from scapy.layers.ntp import NTP
from collections import defaultdict
plik="aim_chat_3a.pcap"
packets = rdpcap("NonVPN-PCAPs-01/"+plik)

layer_counts = defaultdict(int)
print (f"\n=== Analiza pliku "+ plik + " ===")
for pkt in packets:
    for layer in [TCP, UDP, DNS, NTP]:
        if pkt.haslayer(layer):
            layer_counts[layer.__name__] += 1

print("\n=== Zliczanie warstw ===")
for layer, count in layer_counts.items():
    print(f"  {layer}: {count} pakietów")

# Liczniki i listy
udp = 0
tcp = 0
all_ihl = []
all_tos = []
all_len = []
all_frag = []
all_ttl = []
# TCP
all_window_tcp = []
all_dataofs_tcp = []
# UDP
all_len_udp = []

# Przetwarzanie pakietów
for pkt in packets:
    for layer in pkt.layers():
        layer_name = layer.__name__
        if layer_name == "IP":
            layer_instance = pkt.getlayer(layer)
            all_ihl.append(layer_instance.ihl)
            all_tos.append(layer_instance.tos)
            all_len.append(layer_instance.len)
            all_frag.append(layer_instance.frag)
            all_ttl.append(layer_instance.ttl)
        if layer_name == "TCP":
            tcp += 1
            layer_instance = pkt.getlayer(layer)
            all_window_tcp.append(layer_instance.window)
            all_dataofs_tcp.append(layer_instance.dataofs)
        if layer_name == "UDP":
            udp += 1
            layer_instance = pkt.getlayer(layer)
            all_len_udp.append(layer_instance.len)  # Długość pakietu UDP

def analize_list(data):
    if len(data) != 0:
        avg = sum(data) / len(data)
    else:
        avg = 0
    return avg, max(data), min(data)

# Lista analizowanych danych
lists_to_analyze = [
    ("IP IHL", all_ihl),
    ("IP TOS", all_tos),
    ("IP LEN", all_len),
    ("IP FRAG", all_frag),
    ("IP TTL", all_ttl),
    ("TCP WINDOW", all_window_tcp),
    ("TCP DATAOFS", all_dataofs_tcp),
    ("UDP LEN", all_len_udp)  # Dodane poprawnie do analizy
]

# print (f"\n=== Pola ===")
# # Analiza i wyświetlanie wyników
# for name, data in lists_to_analyze:
#     avg, max_val, min_val = analize_list(data)
#     print(f"{name}:")
#     print(f"Średnia: {avg:.2f}")
#     print(f"Max: {max_val}")
#     print(f"Min: {min_val}\n")

for name, data in lists_to_analyze:
    plt.hist(data, bins=20)
    plt.title(f" {plik}: {name}")
    plt.show()

