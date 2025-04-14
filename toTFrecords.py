from scapy.all import rdpcap
import tensorflow as tf
from scapy.layers.dns import DNSRR

TF_ENABLE_ONEDNN_OPTS=0

packets = rdpcap("NonVPN-PCAPs-01/facebook_audio2b.pcapng")

def convert_int64(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))
def extract_packets_info(packet):
    info = {}
    if "IP" in packet:
        info["IP_LEN"] = packet["IP"].len
    return info

tfrecord_file = "packets_data.tfrecords"

with tf.io.TFRecordWriter(tfrecord_file) as writer:
    for packet in packets:
        extracted_info = extract_packets_info(packet)
        print(extracted_info)
        if extracted_info:
            features = {
                key: convert_int64(value)
                for key, value in extracted_info.items()
            }
            example = tf.train.Example(features=tf.train.Features(feature=features))
            writer.write(example.SerializeToString())

# print("Zapisano dane do:", tfrecord_file)