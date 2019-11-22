import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import requests
load_dotenv()

def googleRequestAuthorized(lat,lon,r,keyword):
    '''
    This function allows you to make a request to Google Places API and, given 
    some coordinates and a radius (in meters), returns you all the places that match
    with a keyword (e.g. Starbucks) in that circumference.
    '''
    authToken = os.getenv("GOOGLE_API_TOKEN")
    if not authToken:
        raise ValueError("NECESITAS UN TOKEN")
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&keyword={}&key={}".format(lat,lon,r,keyword,authToken)

    res = requests.get(url)
    data = res.json()
    return data

def add_places(df,place,radius):
    '''
    Given a dataframe and some coordinates, this function will search places that are close 
    to that coordinates in a radius of X meters and will insert them into new columns of the DF.
    '''
    for i in range(len(df)) : 
        lat = df.loc[i, "latitude"]
        lon = df.loc[i, "longitude"]
        answer = googleRequestAuthorized(str(lat),str(lon),str(radius),str(place))
        try:
            df.loc[i, str(place)] = answer['results'][0]['name']
            df.loc[i, str(place)+'_lat'] = answer['results'][0]['geometry']['location']['lat']
            df.loc[i, str(place)+'_lon'] = answer['results'][0]['geometry']['location']['lng']

        except:
            df.loc[i, str(place)] = np.nan
            df.loc[i, str(place)+'_lat'] = np.nan
            df.loc[i, str(place)+'_lon'] = np.nan


# Here I load the DF I created in pymongo.py
startup_clean = pd.read_csv('../input/startups_filtered_mongo.csv')

'''
I will add to my dataframe:
    - Starbucks that are less than 100 m from the startups.
    - Airports that are less than 20 km from the startups.
    - Day Care Centers that are less than 100 m from the startups.
    - Nightclubs that are less than 100 m from the startups.
    - Vegan restaurants that are less than 50 m from the startups.
'''

# Starbucks:
add_places(startup_clean,"starbucks","100")
starbucks_clean = startup_clean.dropna()
starbucks_clean.index = pd.RangeIndex(len(starbucks_clean.index))
starbucks_clean.to_csv('../input/starbucks_without_nan.csv')

# Airport:
add_places(starbucks_clean,"airport","20000")
airports_clean = starbucks_clean.dropna()
airports_clean.index = pd.RangeIndex(len(airports_clean.index))
airports_clean.to_csv('../input/airports_without_nan.csv')

# Day Care Center:
add_places(airports_clean,"daycare","100")
daycare_clean = airports_clean.dropna()
daycare_clean.index = pd.RangeIndex(len(daycare_clean.index))
daycare_clean.to_csv('../input/daycare_without_nan.csv')

# Nightclub:
add_places(daycare_clean,"nightclub","150")
nightclub_clean = daycare_clean.dropna()
nightclub_clean.index = pd.RangeIndex(len(nightclub_clean.index))
nightclub_clean.to_csv('../input/nightclub_without_nan.csv')

# Vegan restaurant:
add_places(nightclub_clean,"vegan+restaurant","50")
all_clean = nightclub_clean.dropna()
all_clean.index = pd.RangeIndex(len(all_clean.index))

# Now I clean and uniform the data in "all_clean" dataframe. For example:
all_clean = all_clean.rename(columns={"vegan+restaurant": "vegan_restaurant", "vegan+restaurant_lat": "vegan_restaurant_lat", "vegan+restaurant_lon": "vegan_restaurant_lon"})
all_clean = all_clean.rename(columns={"name": "tech_startups"})
all_clean['city'] = all_clean['city'].replace({'Copenhagen V':'Copenhagen', 'Montreal, Quebec':'Montreal', 'MontrÃ©al, Qc':'Montreal'})

# Finally, I save it into input folder:
all_clean.to_csv('../input/all_clean.csv')
