# input_screen.py
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import airport_database
from closest_airports import get_airport_data, geocode_city, find_closest_airports, display_on_map
import os
import webbrowser

Builder.load_file("input_screen.kv")

# Define the screens
class InputScreen(Screen):
    def __init__(self, **kwargs):
        super(InputScreen, self).__init__(**kwargs)

    def switch_to_history(self):
        self.manager.current = 'history'

    def find_city(self):
        # Extract city data from input fields
        city_name = self.ids.city_name_input.text
        num_airport = int(self.ids.num_airport_input.text)

        # Store city data in the database
        airport_database.cursor.execute("INSERT INTO cities (name, num_airport) VALUES (?, ?)", (city_name, num_airport))
        city_id = airport_database.cursor.lastrowid
        airport_database.conn.commit()

        self.save_airport_distances(city_name, city_id, num_airport)
        
    def switch_to_map(self):
        city_name = self.ids.city_name_input.text
        self.show_map(city_name)  # Pass the city name to the function

    def show_map(self, city_name):
        airports = get_airport_data()
        city_coords = geocode_city(city_name)
        if city_coords:
            num_airport = int(self.ids.num_airport_input.text)
            closest_airports = find_closest_airports(city_coords, airports, num_airports=num_airport)
            map = display_on_map(city_coords, city_name, closest_airports)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            map_file = os.path.join(current_dir, "closest_airports_map.html")
            map.save(map_file)
            print("Map saved as closest_airports_map.html")
            webbrowser.open(map_file)  # Open the generated HTML file in the default web browser
        else:
            print(f"Could not find the coordinates for the city: {city_name}")

    def save_airport_distances(self, city_name, city_id, num_airports):
        airports = get_airport_data()
        city_coords = geocode_city(city_name)
        if city_coords:
            closest_airports = find_closest_airports(city_coords, airports, num_airports=num_airports)
            for index, airport in closest_airports.iterrows():
                airport_database.cursor.execute("INSERT INTO distances (city_id, airport_id, distance) VALUES (?, ?, ?)", 
                                                (city_id, airport['AirportID'], airport['Distance']))
                airport_database.cursor.execute("INSERT OR IGNORE INTO airports (AirportID, Name, City, Country, IATA, ICAO, Latitude, Longitude, Altitude, Timezone, DST, TzDatabaseTimezone, Type, Source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                                                (airport['AirportID'], airport['Name'], airport['City'], airport['Country'], airport['IATA'], airport['ICAO'], airport['Latitude'], airport['Longitude'], airport['Altitude'], airport['Timezone'], airport['DST'], airport['TzDatabaseTimezone'], airport['Type'], airport['Source']))
            airport_database.conn.commit()
