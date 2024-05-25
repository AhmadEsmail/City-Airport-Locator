#closest_airports.py
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import webbrowser
import os

# Step 1: Fetch airport data
def get_airport_data():
    url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
    airports = pd.read_csv(url, header=None)
    airports.columns = ["AirportID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "TzDatabaseTimezone", "Type", "Source"]
    return airports

# Step 2: Geocode the city to get its latitude and longitude
def geocode_city(city_name):
    geolocator = Nominatim(user_agent="city_locator")
    location = geolocator.geocode(city_name)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# Step 3: Calculate distances and find the closest airports
def find_closest_airports(city_coords, airports, num_airports=5):
    airports['Distance'] = airports.apply(lambda row: geodesic(city_coords, (row['Latitude'], row['Longitude'])).km, axis=1)
    closest_airports = airports.nsmallest(num_airports, 'Distance')
    return closest_airports

# Step 4: Display city and airports on a map
def display_on_map(city_coords, city_name, closest_airports):
    m = folium.Map(location=city_coords, zoom_start=10)
    folium.Marker(location=city_coords, popup=f"City: {city_name}", icon=folium.Icon(color='red')).add_to(m)
    
    for index, airport in closest_airports.iterrows():
        airport_coords = (airport['Latitude'], airport['Longitude'])
        distance = airport['Distance']
        popup_text = f"{airport['Name']} ({airport['IATA']})"
        folium.Marker(location=airport_coords, popup=popup_text, icon=folium.Icon(color='blue')).add_to(m)
        folium.CircleMarker(location=airport_coords, radius=5, color='blue', fill=True, fill_opacity=0.7).add_to(m)
        folium.PolyLine([city_coords, airport_coords], color='green', weight=2.5, opacity=1).add_to(m)
        
        # Calculate the midpoint for placing the distance label
        midpoint_coords = ((city_coords[0] + airport_coords[0]) / 2, (city_coords[1] + airport_coords[1]) / 2)
        
        # Create a DivIcon with custom HTML for the distance label
        label_html = f"<div style='font-size: 14px; color: red;'>{distance:.2f} km</div>"
        folium.map.Marker(
            location=midpoint_coords,
            icon=folium.DivIcon(html=label_html)
        ).add_to(m)
    return m

def main(city_name):
    airports = get_airport_data()
    city_coords = geocode_city(city_name)
    if city_coords:
        closest_airports = find_closest_airports(city_coords, airports)
        map = display_on_map(city_coords, city_name, closest_airports)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        map_file = os.path.join(current_dir, "closest_airports_map.html")
        map.save(map_file)
        print("Map saved as closest_airports_map.html")
        webbrowser.open(map_file)  # Open the generated HTML file in the default web browser
    else:
        print(f"Could not find the coordinates for the city: {city_name}")
