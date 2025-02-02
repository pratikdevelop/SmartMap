import os
import folium
from geopy.geocoders import Nominatim
import requests
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.webview import WebView  # WebView for displaying map
from kivy.garden.webview import WebView as GardenWebView

# Initialize geolocator
geolocator = Nominatim(user_agent="my_map_app")

# Function to get current location using IP
def get_current_location():
    try:
        response = requests.get("https://ipinfo.io/json").json()
        lat, lon = map(float, response["loc"].split(","))
        print(f"Current location: {lat}, {lon}")
        return lat, lon
    except Exception as e:
        print(f"Error retrieving current location: {e}")
        return None

# Function to create and save a map as HTML
def create_map(address):
    location = geolocator.geocode(address)
    if location:
        print(f"Location found: {location.address} at {location.latitude}, {location.longitude}")
        lat, lon = location.latitude, location.longitude
        my_map = folium.Map(location=[lat, lon], zoom_start=15, tiles="cartodbpositron")

        # Add marker
        folium.Marker([lat, lon], popup=location.address, icon=folium.Icon(color="blue")).add_to(my_map)

        # Save map to file
        map_path = os.path.join(os.getcwd(), "map.html")
        my_map.save(map_path)
        return map_path
    return None

# Kivy App
class MapApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10)

        # Label and Text Input
        self.address_input = TextInput(hint_text="Enter Destination", size_hint=(1, 0.1))
        layout.add_widget(self.address_input)

        # Button to generate and show the map
        btn_show_map = Button(text="Show Map", size_hint=(1, 0.1))
        btn_show_map.bind(on_press=self.show_map)
        layout.add_widget(btn_show_map)

        # WebView (for showing the map)
        self.webview = GardenWebView()
        layout.add_widget(self.webview)

        # Get current location
        current_location = get_current_location()
        if current_location:
            lat, lon = current_location
            layout.add_widget(Label(text=f"Current Location: {lat}, {lon}"))
            initial_map_path = create_map(f"{lat}, {lon}")
            if initial_map_path:
                self.webview.url = f'file://{initial_map_path}'

        return layout

    def show_map(self, instance):
        address = self.address_input.text
        if address:
            map_path = create_map(address)
            if map_path:
                self.webview.url = f'file://{map_path}'
            else:
                print("Location not found!")

if __name__ == '__main__':
    MapApp().run()
