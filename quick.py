from scapy.all import rdpcap
from scapy.layers.inet import TCP, UDP
from scapy.layers.dns import DNS
from scapy.layers.ntp import NTP
from scapy.layers.tls.all import TLS, SSLv2
from collections import defaultdict

# Wczytanie pakietów z pliku pcap
packets = rdpcap("NonVPN-PCAPs-01/facebook_audio2b.pcapng")

layer_counts = defaultdict(int)

# Przetwarzanie pakietów
for pkt in packets:
    # Sprawdzenie, czy pakiet zawiera jedną z analizowanych warstw
    for layer in [TCP, UDP, DNS, NTP, TLS, SSLv2]:
        if pkt.haslayer(layer):
            layer_counts[layer.__name__] += 1

            # # Jeśli warstwa TLS lub SSLv2, wyświetl dodatkowe informacje
            # if layer == TLS or layer == SSLv2:
            #     print(f"\n=== Pakiet z warstwą {layer.__name__} ===")
            #     # Wyświetlanie dostępnych parametrów w warstwie
            #     if layer.__name__ == "SSLv2":
            #         # Przykład parametrów TLS/SSL
            #         print(pkt[layer].summary)
            #         print(f"  - Typ: {pkt[layer].type}")
            #         print(f"  - Wersja: {pkt[layer].version}")
            #         print(f"  - Len: {pkt[layer].len}")


# Wyświetlenie liczby pakietów dla każdej warstwy
print("\n=== Zliczanie warstw ===")
for layer, count in layer_counts.items():
    print(f"  {layer}: {count} pakietów")
