# -*- coding: utf-8 -*-
import pandas as pd
from geopy import geocoders

# Load Documents
df = pd.read_csv('Initial Data.csv', encoding='latin-1')

# Create column with required format [Street Name],[Street Number],[Zip Code],[Country]
df['Full_Address'] = df['Full_Adress'] + ', Switzerland'

# Create a Lat column and a Long column. Transform address into lat and long.
df['latitude'] = pd.Series('object')
df['longitude'] = pd.Series('object')

for i in range(len(df['Full_Adress'])):
    try:
        address = df['Full_Adress'][i]
        g = geocoders.GoogleV3(api_key='')  # User your own Google API Key
        location = g.geocode(address, timeout=1)
        df.loc[i, 'latitude'] = location.latitude
        df.loc[i, 'longitude'] = location.longitude
        # print(location.latitude, location.longitude)

    except:
        df.loc[i, 'Latitude'] = 0
        df.loc[i, 'Longitude'] = 0
        print(str(i) + ' Error on address')

# Create csv with energy demand, Latitude, and Longitude.
df_final = df[['P_kW', 'latitude', 'longitude', 'Short_Adress', 'TITRE_IM', 'NOM_IM']]
df_final['Short_Adress'] = df_final['Short_Adress'].str.title()
df_final["Coordinates"] = df[["latitude", "longitude"]].apply(tuple, axis=1)
df_final['Total'] = df_final.groupby(['Coordinates'])['P_kW'].transform('sum')
new_df = df_final.drop_duplicates(subset=['Coordinates'])
#df_final.groupby(["Coordinates"])['P_kW'].sum().reset_index()

new_df.to_csv('demand lat long.csv', index=False)
