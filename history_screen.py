# history_screen.py
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
import airport_database

Builder.load_file("history_screen.kv")

class AirportHistory(Screen):
    def switch_to_input_screen(self):
        self.manager.current = 'input'

    def search_city(self):
        # Get the city name from the text input
        city_name = self.ids.city_name_input.text

        # Check if the city name is provided
        if city_name:
            # Construct the SQL query to search for cities by name
            query = """
            SELECT cities.name, distances.distance, airports.Name 
            FROM cities
            JOIN distances ON cities.id = distances.city_id
            JOIN airports ON distances.airport_id = airports.AirportID
            WHERE cities.name LIKE ?
            """
            airport_database.cursor.execute(query, ('%' + city_name + '%',))
            results = airport_database.cursor.fetchall()

            # Clear any previous search results
            self.ids.search_results_grid.clear_widgets()

            # Display search results in the grid layout
            if results:
                for city, distance, airport in results:
                    self.ids.search_results_grid.add_widget(Label(text=f"City: {city}"))
                    self.ids.search_results_grid.add_widget(Label(text=f"Airport: {airport}"))
                    self.ids.search_results_grid.add_widget(Label(text=f"Distance: {distance:.2f} km"))
            else:
                self.ids.search_results_grid.add_widget(Label(text="No results found."))
        else:
            print("Please enter a city name.")
