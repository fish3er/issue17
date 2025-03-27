from scipy.io import arff
import pandas as pd

# data - the data in the arff file
# meta - the meta data of the arff file ( the attributes and their types)
data, meta = arff.loadarff("Scenario A1-ARFF/Scenario A1-ARFF/TimeBasedFeatures-Dataset-15s-VPN.arff")

df = pd.DataFrame(data)


print(df)
print(len(df))