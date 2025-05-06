import tensorflow as tf

# Ścieżka do pliku .tfrecords
tfrecord_file = "AIMchat2.pcapng"

# Funkcja do wczytywania rekordów
def parse_example(example_proto):
    # Można zdefiniować sztywno znane pola — ale tu robimy ogólne odczytanie
    return tf.io.parse_single_example(example_proto, {
        # Używamy "catch-all" dla int64 - wszystko, co zostało zapisane jako int64
        key: tf.io.FixedLenFeature([], tf.int64)
        for key in tf.io.parse_single_example(example_proto, {}).keys()
    })

# Alternatywna metoda – bez określania schematu (do testów)
raw_dataset = tf.data.TFRecordDataset([tfrecord_file])

# Dekodowanie przykładów i wyświetlenie kilku z nich
for raw_record in raw_dataset.take(5):  # Tylko 5 przykładów na start
    example = tf.train.Example()
    example.ParseFromString(raw_record.numpy())
    print("---- Nowy pakiet ----")
    for key, feature in example.features.feature.items():
        value = feature.int64_list.value[0] if feature.HasField("int64_list") else None
        print(f"{key}: {value}")
