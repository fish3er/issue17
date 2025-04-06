from scapy.all import rdpcap

# Wczytanie pliku .pcap
packets = rdpcap("NonVPN-PCAPs-01/aim_chat_3b.pcap")

# Liczniki i listy
udp = 0
tcp = 0
all_ihl = []
all_tos = []
all_len = []
all_id = []
all_frag = []
all_ttl = []
all_proto = []
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
            all_id.append(layer_instance.id)
            all_frag.append(layer_instance.frag)
            all_ttl.append(layer_instance.ttl)
            all_proto.append(layer_instance.proto)
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
    ("IHL", all_ihl),
    ("TOS", all_tos),
    ("LEN", all_len),
    ("ID", all_id),
    ("FRAG", all_frag),
    ("TTL", all_ttl),
    ("PROTO", all_proto),
    ("TCP WINDOW", all_window_tcp),
    ("TCP DATAOFS", all_dataofs_tcp),
    ("UDP LEN", all_len_udp)  # Dodane poprawnie do analizy
]

# Analiza i wyświetlanie wyników
for name, data in lists_to_analyze:
    avg, max_val, min_val = analize_list(data)
    print(f"{name}:")
    print(f"  ➤ Średnia: {avg:.2f}")
    print(f"  ➤ Max: {max_val}")
    print(f"  ➤ Min: {min_val}\n")

# Wyświetlanie liczby pakietów TCP i UDP
print(f"Łączna liczba pakietów TCP: {tcp}")
print(f"Łączna liczba pakietów UDP: {udp}")
