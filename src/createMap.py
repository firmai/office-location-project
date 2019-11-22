import folium
import pandas as pd

all_clean = pd.read_csv('./output/all_clean.csv')

def generateMap(city):
    city_df = all_clean.loc[all_clean.city == city]
    lati = city_df['latitude'].iloc[0]
    long = city_df['longitude'].iloc[0]
    map_city=folium.Map(location=[float(lati),float(long)], zoom_start=12)

    for index, row in city_df.iterrows():
        folium.Marker((row['latitude'],row['longitude']),
                        radius=2,
                        icon=folium.Icon(icon='home',color='red'),
                        tooltip='Cool Tech Startup: '+str(row['tech_startups'])
                    ).add_to(map_city)
        
    for index, row in city_df.iterrows():
        folium.Marker((row['starbucks_lat'],row['starbucks_lon']),
                        radius=2,
                        icon=folium.Icon(icon='leaf',color='green'),
                        tooltip=str(row['starbucks'])
                    ).add_to(map_city)
        
    for index, row in city_df.iterrows():
        folium.Marker((row['air_lat'],row['air_lon']),
                        radius=2,
                        icon=folium.Icon(icon='plane',color='lightgray'),
                        tooltip=str(row['airport'])
                    ).add_to(map_city)
        
        
    for index, row in city_df.iterrows():
        folium.Marker((row['daycare_lat'],row['daycare_lon']),
                        radius=2,
                        icon=folium.Icon(icon='heart',color='blue'),
                        tooltip='Kindergarten: '+str(row['daycare'])
                    ).add_to(map_city)
        
        
    for index, row in city_df.iterrows():
        folium.Marker((row['nightclub_lat'],row['nightclub_lon']),
                        radius=2,
                        icon=folium.Icon(icon='glass',color='darkpurple'),
                        tooltip='Nightclub: '+str(row['nightclub'])
                    ).add_to(map_city)
        
    for index, row in city_df.iterrows():
        folium.Marker((row['vegan_restaurant_lat'],row['vegan_restaurant_lon']),
                        radius=2,
                        icon=folium.Icon(icon='cutlery',color='darkgreen'),
                        tooltip='Vegan: '+str(row['vegan_restaurant'])
                    ).add_to(map_city)
    return map_city