# main.py

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from input_screen import InputScreen
from history_screen import AirportHistory
from custom_button import CustomButton
import airport_database

# Load the Kivy files
Builder.load_file("input_screen.kv")
Builder.load_file("history_screen.kv")

# Define the screen manager
class ScreenManagerApp(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagerApp, self).__init__(**kwargs)

        # Add screens to the screen manager
        self.add_widget(InputScreen(name='input'))
        self.add_widget(AirportHistory(name='history'))

class MapApp(App):
    def build(self):
        return ScreenManagerApp()

if __name__ == '__main__':
    MapApp().run()
