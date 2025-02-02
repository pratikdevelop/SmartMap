# import folium
# import osmnx as ox
# import networkx as nx
# import tkinter as tk
# from tkinter import messagebox
# from tkinterweb import HtmlFrame  # For displaying map inside Tkinter
# from geopy.geocoders import Nominatim
# import requests
# import os

# # Initialize geolocator
# geolocator = Nominatim(user_agent="my_map_app")

# # Function to get current location using IP
# def get_current_location():
#     try:
#         response = requests.get("https://ipinfo.io/json").json()
#         lat, lon = map(float, response["loc"].split(","))
#         print(f"Current location: {lat}, {lon}")
#         return lat, lon
#     except Exception as e:
#         print(f"Error retrieving current location: {e}")
#         return None

# # Function to create and display a location on the map
# def show_location():
#     address = entry.get()
#     if not address:
#         messagebox.showerror("Error", "Please enter a location.")
#         return
    
#     location = geolocator.geocode(address)
#     if location:
#         print(f"Location found: {location.address} at {location.latitude}, {location.longitude}")
#         lat, lon = location.latitude, location.longitude
#         my_map = folium.Map(location=[lat, lon], zoom_start=15, tiles="cartodbpositron")

#         # Add marker
#         folium.Marker([lat, lon], popup=location.address, icon=folium.Icon(color="blue")).add_to(my_map)

#         # Save the map to a file and update the display
#         save_map_to_file(my_map)
#     else:
#         messagebox.showerror("Error", "Location not found!")

# # Function to save the map to a file
# def save_map_to_file(folium_map):
#     # Get absolute path for map file
#     map_path = os.path.join(os.getcwd(), "index.html")  # Using the current working directory
#     folium_map.save(map_path)
    
#     # Load the saved map file into the HTML frame
#     load_map_from_file(map_path)

# # Function to load the map from a saved HTML file
# def load_map_from_file(file_path):
#     if os.path.exists(file_path):
#         print(f"Loading map from: {file_path}")  # Debugging line to check the file path
#         map_frame.load_url(f"file://{file_path}")  # Load the file via absolute path
#     else:
#         messagebox.showerror("Error", "Map file not found!")

# # Tkinter GUI Setup
# root = tk.Tk()
# root.title("Google Maps Alternative")
# root.geometry("800x600")

# # Input Field
# tk.Label(root, text="Enter Destination:").pack(pady=5)
# entry = tk.Entry(root, width=40)
# entry.pack(pady=5)

# # Buttons
# tk.Button(root, text="Show Location", command=show_location).pack(pady=5)

# # Frame for Map Display
# map_frame = HtmlFrame(root, width=750, height=500, messages_enabled=False)
# map_frame.pack(pady=10)

# # Load Initial Map
# current_location = get_current_location()
# if current_location:
#     lat, lon = current_location
#     initial_map = folium.Map(location=[lat, lon], zoom_start=12, tiles="cartodbpositron")
#     save_map_to_file(initial_map)

# root.mainloop()

import folium
import osmnx as ox
import networkx as nx
import tkinter as tk
from tkinter import messagebox
from tkinterweb import HtmlFrame  # For displaying map inside Tkinter
from geopy.geocoders import Nominatim
import requests
import os

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

# Function to create and display a location on the map
def show_location():
    address = entry.get()
    if not address:
        messagebox.showerror("Error", "Please enter a location.")
        return
    
    location = geolocator.geocode(address)
    if location:
        print(f"Location found: {location.address} at {location.latitude}, {location.longitude}")
        lat, lon = location.latitude, location.longitude
        my_map = folium.Map(location=[lat, lon], zoom_start=15, tiles="cartodbpositron")

        # Add marker
        folium.Marker([lat, lon], popup=location.address, icon=folium.Icon(color="blue")).add_to(my_map)

        # Save the map to a file and update the display
        save_map_to_file(my_map)
    else:
        messagebox.showerror("Error", "Location not found!")

# Function to save the map to a file
def save_map_to_file(folium_map):
    # Get absolute path for map file
    map_path = os.path.join(os.getcwd(), "map.html")  # Using the current working directory
    folium_map.save(map_path)
    
    # Load the saved map file into the HTML frame
    load_map_from_file(map_path)

# Function to load the map from a saved HTML file
def load_map_from_file(file_path):
    if os.path.exists(file_path):
        print(f"Loading map from: {file_path}")  # Debugging line to check the file path
        map_frame.load_url(f"file://{file_path}")  # Load the file via absolute path
        map_frame.update()  # Force update/re-rendering of the map in the Tkinter window
    else:
        messagebox.showerror("Error", "Map file not found!")

# Tkinter GUI Setup
root = tk.Tk()
root.title("Google Maps Alternative")
root.geometry("800x600")

# Input Field
tk.Label(root, text="Enter Destination:").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# Buttons
tk.Button(root, text="Show Location", command=show_location).pack(pady=5)

# Frame for Map Display
map_frame = HtmlFrame(root, width=750, height=500, messages_enabled=False)
map_frame.pack(pady=10)

# Load Initial Map
current_location = get_current_location()
if current_location:
    lat, lon = current_location
    initial_map = folium.Map(location=[lat, lon], zoom_start=12, tiles="cartodbpositron")
    save_map_to_file(initial_map)

root.mainloop()
