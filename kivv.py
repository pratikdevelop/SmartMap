import os
import json
import requests
from geopy.geocoders import Nominatim
import webview
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder

# Define the layout for SuggestionList and SuggestionButton using Kivy language
Builder.load_string('''
<SuggestionButton@Button>:
    on_release: app.select_suggestion(self.text)

<SuggestionList>:
    viewclass: 'SuggestionButton'
    RecycleBoxLayout:
        default_size: None, dp(40)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')

# Initialize geolocator
geolocator = Nominatim(user_agent="SmartMap")

def get_current_location():
    try:
        response = requests.get("https://ipinfo.io/json").json()
        lat, lon = map(float, response["loc"].split(","))
        return lat, lon
    except Exception as e:
        print(f"Error retrieving current location: {e}")
        return None

class SuggestionList(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        
    def update_suggestions(self, suggestions):
        self.data = [{'text': suggestion} for suggestion in suggestions]

class Api:
    def map_clicked(self, lat, lon):
        print(f"Map clicked at {lat}, {lon}")
        # Optionally, add a marker or perform reverse geocoding here

class MapApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10)
        
        # Start location input
        self.start_input = TextInput(hint_text="Enter Start Location", size_hint=(1, 0.1))
        layout.add_widget(self.start_input)
        
        # Destination input
        self.address_input = TextInput(hint_text="Enter Destination", size_hint=(1, 0.1))
        self.address_input.bind(text=self.update_suggestions)
        layout.add_widget(self.address_input)
        
        # Suggestions list
        self.suggestion_list = SuggestionList(size_hint=(1, 0.3))
        layout.add_widget(self.suggestion_list)
        
        # Button to show map
        btn_show_map = Button(text="Show Map", size_hint=(1, 0.1))
        btn_show_map.bind(on_press=self.show_map)
        layout.add_widget(btn_show_map)
        
        # Button to show route
        btn_show_route = Button(text="Show Route", size_hint=(1, 0.1))
        btn_show_route.bind(on_press=self.show_route)
        layout.add_widget(btn_show_route)
        
        # Create webview window
        map_path = os.path.join(os.getcwd(), "map.html")
        api = Api()
        self.webview_window = webview.create_window("SmartMap", f"file://{map_path}", width=800, height=600, js_api=api)
        
        # Start webview with gui='kivy' to integrate with Kivy's event loop
        self.start_webview()

        return layout
    
    def start_webview(self):
        # Start the webview in a separate thread and set initial location afterward
        webview.start(gui='kivy')
        current_location = get_current_location()
        if current_location:
            lat, lon = current_location
            js_code = f"setView({lat}, {lon}, 15); addMarker({lat}, {lon}, 'Current Location');"
            # Wait briefly for the webview to load (not ideal, but works for now)
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.webview_window.evaluate_javascript(js_code), 1)
    
    def update_suggestions(self, instance, text):
        if not text:
            self.suggestion_list.update_suggestions([])
            return
        locations = geolocator.geocode(text, exactly_one=False, limit=5)
        if locations:
            suggestions = [location.address for location in locations]
            self.suggestion_list.update_suggestions(suggestions)
    
    def select_suggestion(self, suggestion_text):
        self.address_input.text = suggestion_text
        self.suggestion_list.update_suggestions([])
    
    def show_map(self, instance):
        address = self.address_input.text
        if address:
            location = geolocator.geocode(address)
            if location:
                lat, lon = location.latitude, location.longitude
                js_code = f"addMarker({lat}, {lon}, '{address}'); setView({lat}, {lon}, 15);"
                self.webview_window.evaluate_javascript(js_code)
    
    def show_route(self, instance):
        start_address = self.start_input.text
        dest_address = self.address_input.text
        if start_address and dest_address:
            start_location = geolocator.geocode(start_address)
            dest_location = geolocator.geocode(dest_address)
            if start_location and dest_location:
                start_lat, start_lon = start_location.latitude, start_location.longitude
                dest_lat, dest_lon = dest_location.latitude, dest_location.longitude
                url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{dest_lon},{dest_lat}?geometries=geojson"
                response = requests.get(url)
                if response.status_code == 200:
                    route_data = response.json()
                    if route_data['code'] == 'Ok':
                        geojson = route_data['routes'][0]['geometry']
                        js_code = f"addRoute('{json.dumps(geojson)}');"
                        self.webview_window.evaluate_javascript(js_code)

if __name__ == '__main__':
    MapApp().run()