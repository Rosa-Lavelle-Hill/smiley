import pandas as pd
import json

df = pd.read_csv("data/100268.csv", sep=';')

# select columns
cols = ['ID Standort', 'Strassenname',
       'Zeitpunkt Messung', 'Messung Datum', 'Messung Zeit',
       'Einfahrtstempo', 'Ausfahrtstempo', 'Differenztempo', 'Tempolimit',
       'Halterung']

df = df[cols]

# rename columns
cols_eng = ['ID location', 'Street name',
       'Time measurement', 'Measurement date', 'Measurement time',
       'Entry speed', 'Exit speed', 'Difference speed', 'Speed limit',
       'Permanent']

df.columns = cols_eng

# select random sample
df = df.sample(n=5000)

# Extract time
df['Hour'] = df['Timestamp'].dt.hour



df.to_csv("data_preprocessed.csv")

print('done')

