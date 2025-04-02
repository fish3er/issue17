from scapy.all import rdpcap

packets = rdpcap("NonVPN-PCAPs-01/aim_chat_3a.pcap")

# Iteracja przez pierwsze 10 pakietów (dla lepszej czytelności)
for i, pkt in enumerate(packets):
    print(f"\n Pakiet {i + 1}:")

    for layer in pkt.layers():
        layer_name = layer.__name__
        print(f"  🏷 Warstwa: {layer_name}")

        # Pobranie pól i wartości dla każdego pakietu
        layer_instance = pkt.getlayer(layer)
        for field_name, field_value in layer_instance.fields.items():
            print(f"  {field_name}: {field_value}")
