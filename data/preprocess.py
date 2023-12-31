import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv("Basel_data.csv", sep=';')

# select random sample
df = df.sample(n=500)

# select columns
cols = ['ID Standort', 'Strassenname',
        'Messung Datum', 'Messung Zeit',
       'Einfahrtstempo', 'Ausfahrtstempo', 'Differenztempo', 'Tempolimit',
       'Halterung']

df = df[cols]

# rename columns
cols_eng = ['ID location', 'Street name',
       'Date', 'Time',
       'Entry speed', 'Exit speed', 'Difference speed', 'Speed limit',
       'Permanent']

df.columns = cols_eng

# Extract hour
df['Hour'] = df['Time'].str.split(':').str[0]
df['Hour'] = df['Hour'].astype(int)

# Extract minute
df['Minutes'] = df['Time'].str.split(':').str[1]
df['Minutes'] = df['Minutes'].astype(int)

# Extract month
df['Month'] = df['Date'].str.split('-').str[1]
df['Month'] = df['Month'].astype(int)

# Extract day of month
df['DoM'] = df['Date'].str.split('-').str[2]
df['DoM'] = df['DoM'].astype(int)

# Print/plot simple descriptives of IVs
print(df["ID location"].value_counts())

print(df["Permanent"].value_counts())

print(df["Speed limit"].value_counts())

df['Hour'].plot(kind='hist', bins=20, edgecolor='black')
plt.xlabel('Hour')
plt.savefig("hour.png")
plt.close()

df['Minutes'].plot(kind='hist', bins=20, edgecolor='black')
plt.xlabel('Minutes past hour')
plt.savefig("min.png")
plt.close()

df['DoM'].plot(kind='hist', bins=20, edgecolor='black')
plt.xlabel('Day of Month')
plt.savefig("DoM.png")
plt.close()

df['Month'].plot(kind='hist', bins=20, edgecolor='black')
plt.xlabel('Month')
plt.savefig("month.png")
plt.close()

# y
df['Difference speed'].plot(kind='hist', bins=20, edgecolor='black')
plt.xlabel('Speed Difference')
plt.savefig("y.png")
plt.close()

# Select IVs + y
final_variables = ['Street name', 'Speed limit', 'Permanent', 'Hour', 'Minutes', 'Month', 'DoM', 'Difference speed']
df = df[final_variables]

df.to_csv("data_preprocessed.csv")

print('done')

