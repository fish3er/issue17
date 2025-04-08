import os
from scapy.all import rdpcap
from scapy.layers.inet import TCP, UDP
from scapy.layers.dns import DNS
from scapy.layers.ntp import NTP
from scapy.layers.tls.all import TLS, SSLv2
from collections import defaultdict
import matplotlib.pyplot as plt

# Ścieżka do folderu z plikami pcap
folder_path = "NonVPN-PCAPs-01"

for filename in os.listdir(folder_path):
    if filename.endswith(".pcap") or filename.endswith(".pcapng"):
        file_path = os.path.join(folder_path, filename)
        packets = rdpcap(file_path)

        # Liczniki i listy
        udp = 0
        tcp = 0
        all_ihl = []
        all_tos = []
        all_len = []
        all_frag = []
        all_ttl = []
        all_window_tcp = []
        all_dataofs_tcp = []
        all_len_udp = []
        all_tls_type = []
        all_ttl_version = []
        all_ssl_type = []
        layer_counts = defaultdict(int)

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
                    all_len_udp.append(layer_instance.len)
                if layer_name == "TLS":
                    layer_instance = pkt.getlayer(layer)
                    try:
                        all_tls_type.append(layer_instance.type)
                    except AttributeError:
                        all_tls_type.append(0)
                    try:
                        all_ttl_version.append(layer_instance.version)
                    except AttributeError:
                        all_ttl_version.append(0)
                if layer_name == "SSLv2":
                    layer_instance = pkt.getlayer(layer)
                    try:
                        all_ssl_type.append(layer_instance.type)
                    except AttributeError:
                        all_ssl_type.append(0)

            for layer in [TCP, UDP, DNS, NTP, TLS, SSLv2]:
                if pkt.haslayer(layer):
                    layer_counts[layer.__name__] += 1

        lists_to_analyze = [
            ("IHL", all_ihl),
            ("TOS", all_tos),
            ("LEN", all_len),
            ("FRAG", all_frag),
            ("TTL", all_ttl),
            ("TCP WINDOW", all_window_tcp),
            ("TCP DATAOFS", all_dataofs_tcp),
            ("UDP LEN", all_len_udp),
            ("TLS TYPE", all_tls_type),
            ("TLS VERSION", all_ttl_version)
        ]


        for name, data in lists_to_analyze:
            plt.hist(data, bins=20)
            plt.title(f" {filename}: {name}")
            plt.show()
