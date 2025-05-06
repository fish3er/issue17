from scapy.all import rdpcap, IP, TCP, UDP
import tensorflow as tf

TF_ENABLE_ONEDNN_OPTS = 0  # dla ograniczenia warningów (opcjonalne)

packets = rdpcap("NonVPN-PCAPs-01/facebookchat3.pcapng")

#konwersja pól
def convert_int64(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

# ekstrakcaj pól
def extract_fields(layer):

    info = {}
    for field in layer.fields_desc:
        field_name = field.name
        try:
            value = getattr(layer, field_name)
            if isinstance(value, int):
                info[field_name.upper()] = value
        except Exception:
            continue  # ignoruj nieobsługiwane pola
    return info


def extract_packets_info(packet, last_time):
    info = {}

    # Czas i delta
    current_time = float(packet.time)
    delta_time = current_time - last_time if last_time else 0.0
    info["DELTA_TIME_US"] = int(delta_time * 1e6)  # mikrosekundy

    # Całkowita długość pakietu
    info["PACKET_LEN"] = len(packet)

    # IP warstwa
    if IP in packet:
        info.update({f"IP_{k}": v for k, v in extract_fields(packet[IP]).items()})

    # TCP lub UDP warstwa
    if TCP in packet:
        info.update({f"TCP_{k}": v for k, v in extract_fields(packet[TCP]).items()})
    elif UDP in packet:
        info.update({f"UDP_{k}": v for k, v in extract_fields(packet[UDP]).items()})

    return info, current_time


tfrecord_file = "facebookchat3.tfrecords"
last_time = None

with tf.io.TFRecordWriter(tfrecord_file) as writer:
    for packet in packets:
        extracted_info, last_time = extract_packets_info(packet, last_time)
        features = {
            key: convert_int64(value)
            for key, value in extracted_info.items()
        }
        example = tf.train.Example(features=tf.train.Features(feature=features))
        writer.write(example.SerializeToString())

print("Zapisano dane do:", tfrecord_file)