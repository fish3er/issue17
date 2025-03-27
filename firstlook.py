import seaborn as sns
from matplotlib import pyplot as plt
from scipy.io import arff
import pandas as pd
# data enrypted trafic with 14 labels
#7 for regular encrypted traffic and 7 for VPN traffic
# data - the data in the arff file
# meta - the metadata of the arff file ( the attributes and their types)
data, meta = arff.loadarff("Scenario A1-ARFF/Scenario A1-ARFF/TimeBasedFeatures-Dataset-15s-VPN.arff")
df = pd.DataFrame(data)
# both typem VPN and Non-VPN trafic
#duration - duration of the flow
#fiat - forward inter arrival time  the time between two packets sent forward direction
#biat  - Backward Inter Arrival Time, the time between two packets sent backwards
#flowiat -  Flow Inter Arrival Time, the time between two packets sent in either direction
#active - The amount of time  a flow was active before going idle
#idle - The amount of time a flow was idle before becoming active
#fb_psec - Flow Bytes per second
#fp_psec - Flow packets per second
features = meta.names()

# print(features)
# print(df.head())

# duration
duration=df['duration']
duration_stats=duration.describe()
print(f"Mediana: {duration_stats['mean']}")  # Mediana
print(f"IQR: {duration_stats['75%']-duration_stats['25%']}")  # rozstęp między kwantylowy
print(f"Standard deviation: {duration_stats["std"]}")
# plt.figure(figsize=(10, 5))
# sns.kdeplot(duration)
# plt.title("Rozkład gęstości długości ruchu") # nie wiem do końca jak to nazwać, wyrysowałem ilości próbek w zależności ich długości
# plt.xlabel("Długość")
# plt.ylabel("Ilość próbek ? ")
# plt.show()


# for feature in features[:-1]:
#     correlation = duration.corr(df[feature])
#     print(f"Korelacja między duration a {feature}: {correlation:.2f}")
#
# plt.figure(figsize=(10, 5))
# plt.plot(duration, df["max_flowiat"])
# plt.show()

# corr for all
# for feature in features[:-1]:
#     for feature2 in features[:-1]:
#         correlation = df[feature2].corr(df[feature])
#         if feature!= feature2 and correlation > 0.9:
#             print(f"Korelacja między {feature} a {feature2}: {correlation:.2f}")
dfstripped = df.iloc[:, :-1] # .iloc[wiersz, kolumna]
corrmatrix=dfstripped.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corrmatrix, annot=False, cmap="coolwarm", center=0, linewidths=0.5, vmin=-1, vmax=1)

plt.title("Mapa korelacji cech")
plt.show()

