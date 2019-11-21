from pymongo import MongoClient
import numpy as np
import pandas as pd

# Let's connect to the database and collection we want to in our localhost:

def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

db, coll = connectCollection('companies','companies')

# I am going to filter all companies that have been founded after 2003, that have raised at least 1M dollars and that have a category code similar to a gaming company.

pipeline = [
    { "$unwind": "$offices"},
    {"$match":{ "$and": [  {"founded_year":{"$gt":2003}},
            {"funding_rounds.raised_amount":{"$gt":1000000}}, { "$or":[{"category_code":"web"},
            {"category_code":"software"},{"category_code":"games_video"},
            {"category_code":"hardware"},{"category_code":"mobile"},{"category_code":"music"},
            {"category_code":"photo_video"},{"category_code":"design"}]}] }}

    ]
results = list(coll.aggregate(pipeline))

# Now I am going to put all this data into a Pandas dataframe:

name = []
city = []
country_code = []
longitude = []
latitude = []

for e in results:
    name.append(e["name"])
    city.append(e['offices']["city"])
    country_code.append(e['offices']["country_code"])
    for c in e["offices"].items():
        if c[0]=="longitude":
            longitude.append(c[1])
        elif c[0]=="latitude":
            latitude.append(c[1])

myData = {"name":name, "city":city, "country":country_code, "latitude":latitude, "longitude":longitude}
startup_df = pd.DataFrame(data=myData)

# At this point I could use geocoding to obtain the null coordinates with the address of each offices, but for simplifying purposes, I am going to get rid of them.

startup_clean = startup_df.dropna()
startup_clean.index = pd.RangeIndex(len(startup_clean.index))

# Save the dataframe with all tech startups that have been founded after 2003 and have raised more than 1M.
startup_clean.to_csv(r'./input/startups_filtered_mongo.csv')