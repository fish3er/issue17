from scapy.all import rdpcap

# Wczytanie pliku .pcap
packets = rdpcap("NonVPN-PCAPs-01/aim_chat_3a.pcap")

# Iteracja przez pakiety i wypisanie ich numerów
for i, pkt in enumerate(packets, 1):  # Enumerate zaczyna liczenie od 1
    # print(f"Pakiet {i}: {pkt.summary()}")

    # Sprawdzenie, czy pakiet ma warstwę UDP
    if pkt.haslayer("UDP"):
        udp_layer = pkt.getlayer("UDP")
        print("UDP Layer:")
        print(f"  ➤ Sport: {udp_layer.sport}")
        print(f"  ➤ Dport: {udp_layer.dport}")
        print(f"  ➤ Len: {udp_layer.len}")
        print(f"  ➤ Chksum: {udp_layer.chksum}")
