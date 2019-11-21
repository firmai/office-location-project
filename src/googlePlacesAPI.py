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


# Fro