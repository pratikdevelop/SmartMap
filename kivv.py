import os
import folium
from geopy.geocoders import Nominatim
import requests
import webview
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.lang import Builder

# Define the layout for SuggestionList and a custom SuggestionButton using Kivy language
Builder.load_string('''
<SuggestionButton@Button>:
    # When a suggestion is clicked, call the app's select_suggestion method with the button text
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

def create_map(address):
    location = geolocator.geocode(address)
    if location:
        lat, lon = location.latitude, location.longitude
        my_map = folium.Map(location=[lat, lon], zoom_start=15, tiles="cartodbpositron")
        folium.Marker([lat, lon], popup=location.address, icon=folium.Icon(color="blue")).add_to(my_map)
        map_path = os.path.join(os.getcwd(), "map.html")
        my_map.save(map_path)
        return map_path
    return None

class SuggestionList(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        
    def update_suggestions(self, suggestions):
        self.data = [{'text': suggestion} for suggestion in suggestions]

class MapApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10)
        
        # Input for destination
        self.address_input = TextInput(hint_text="Enter Destination", size_hint=(1, 0.1))
        self.address_input.bind(text=self.update_suggestions)
        layout.add_widget(self.address_input)
        
        # Suggestions list using RecycleView
        self.suggestion_list = SuggestionList(size_hint=(1, 0.3))
        layout.add_widget(self.suggestion_list)
        
        # Button to display map
        btn_show_map = Button(text="Show Map", size_hint=(1, 0.1))
        btn_show_map.bind(on_press=self.show_map)
        layout.add_widget(btn_show_map)
        
        # Show current location map if available
        current_location = get_current_location()
        if current_location:
            lat, lon = current_location
            layout.add_widget(Label(text=f"Current Location: {lat}, {lon}"))
            initial_map_path = create_map(f"{lat}, {lon}")
            if initial_map_path:
                self.show_in_webview(initial_map_path)
        return layout
    
    def update_suggestions(self, instance, text):
        # Clear suggestions if text is empty
        if not text:
            self.suggestion_list.update_suggestions([])
            return
        # Get up to 5 location suggestions based on the text input
        locations = geolocator.geocode(text, exactly_one=False, limit=5)
        if locations:
            suggestions = [location.address for location in locations]
            self.suggestion_list.update_suggestions(suggestions)
    
    def select_suggestion(self, suggestion_text):
        # When a suggestion is clicked, update the text input and clear the suggestion list
        self.address_input.text = suggestion_text
        self.suggestion_list.update_suggestions([])
    
    def show_map(self, instance):
        address = self.address_input.text
        if address:
            map_path = create_map(address)
            if map_path:
                self.show_in_webview(map_path)
    
    def show_in_webview(self, map_path):
        webview.create_window("Map Viewer", f"file://{map_path}")
        webview.start()

if __name__ == '__main__':
    MapApp().run()
