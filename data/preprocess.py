import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_csv("Basel_data.csv", sep=';')

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

# find those speeding before
df = df[df['Entry speed'] > df['Speed limit']]

# create binary y
df['Speeding after'] = 0
df['Speeding after'][df['Exit speed'] > df['Speed limit']] = 1

# select random sample stratified by y
sample_size = 5000
df = df.groupby('Speeding after', group_keys=False).apply(lambda x: x.sample(min(len(x), sample_size)))
print(df['Speeding after'].value_counts())

# Extract hour
df['Hour'] = df['Time'].str.split(':').str[0]
df['Hour'] = df['Hour'].astype(int)

# Extract minute
df['Minutes'] = df['Time'].str.split(':').str[1]
df['Minutes'] = df['Minutes'].astype(int)

# Extract month
df['Month'] = df['Date'].str.split('-').str[1]
df['Month'] = df['Month'].astype(int)
df['Month'].replace({3:'March', 4: 'April', 5: 'May', 6: 'June'}, inplace=True)

# Extract day of week
def get_day_of_week(date_string):
    """Function to get day of the week from a date string"""
    date_object = datetime.strptime(date_string, '%Y-%m-%d')
    return date_object.strftime('%A')  # Return the day name

# Apply the function to the entire column
df['Day of Week'] = df['Date'].apply(get_day_of_week)

# Print/plot simple descriptives of IVs
print(df["ID location"].value_counts())

print(df["Permanent"].value_counts())

print(df["Speed limit"].value_counts())

plot_save_path = "plots/"
df['Hour'].plot(kind='hist', bins=20, edgecolor='black')
plt.xlabel('Hour')
plt.savefig(plot_save_path + "hour.png")
plt.close()

df['Minutes'].plot(kind='hist', bins=20, edgecolor='black')
plt.xlabel('Minutes past hour')
plt.savefig(plot_save_path + "min.png")
plt.close()

df['Day of Week'].value_counts().plot(kind='bar')
plt.xlabel('Day of Week')
plt.tight_layout()
plt.savefig(plot_save_path + "day_of_week.png")
plt.close()

df['Month'].value_counts().plot(kind='bar')
plt.xlabel('Month')
plt.tight_layout()
plt.savefig(plot_save_path + "month.png")
plt.close()

# y
df['Difference speed'].plot(kind='hist', bins=20, edgecolor='black')
plt.xlabel('Speed Difference')
plt.savefig(plot_save_path + "y_diff.png")
plt.close()

# plot y binary
df['Speeding after'].value_counts().plot(kind='bar')
plt.xlabel('Speeding after')
plt.xticks(rotation=0)
plt.savefig(plot_save_path + "y_binary.png")
plt.close()

# Select IVs + y
final_variables = ['Street name', 'Speed limit', 'Permanent', 'Hour', 'Minutes', 'Month', 'Day of Week', 'Speeding after']
df = df[final_variables]

# OHE IVs
one_hot_encoded = pd.get_dummies(df, columns=df.select_dtypes(include='object').columns)

# change names
col_list = list(one_hot_encoded.columns)
new_col_list = [item.split('_')[-1] for item in col_list]

one_hot_encoded.columns = new_col_list
one_hot_encoded.drop('mobil', axis=1, inplace=True)
one_hot_encoded.rename(columns={'permanent' : "Permanent"}, inplace=True)

one_hot_encoded = one_hot_encoded.replace({True: 1, False: 0})

one_hot_encoded.to_csv("data_preprocessed.csv")

one_hot_encoded.to_json('data_preprocessed.json', orient='records')

print('done')

