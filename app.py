# import folium
# import osmnx as ox
# import networkx as nx
# import tkinter as tk
# from tkinter import messagebox
# from tkinterweb import HtmlFrame  # For displaying map directly in Tkinter
# from geopy.geocoders import Nominatim
# import requests
# import io
# import sys

# # Initialize geolocator
# geolocator = Nominatim(user_agent="my_map_app")

# # Function to get current location using IP
# def get_current_location():
#     try:
#         response = requests.get("https://ipinfo.io/json").json()
#         lat, lon = map(float, response["loc"].split(","))
#         return lat, lon
#     except:
#         return None

# # Function to create and display the map dynamically in Tkinter
# def show_map(address):
#     location = geolocator.geocode(address)
#     if location:
#         lat, lon = location.latitude, location.longitude
#         my_map = folium.Map(location=[lat, lon], zoom_start=15, tiles="cartodbpositron")

#         # Add marker
#         folium.Marker([lat, lon], popup=location.address).add_to(my_map)

#         # Render the map dynamically
#         update_map(my_map)
#     else:
#         messagebox.showerror("Error", "Location not found!")

# # Function to find directions from current location
# def find_directions(destination):
#     current_location = get_current_location()
#     if not current_location:
#         messagebox.showerror("Error", "Could not fetch current location!")
#         return

#     start_lat, start_lon = current_location
#     location = geolocator.geocode(destination)
#     if location:
#         end_lat, end_lon = location.latitude, location.longitude

#         # Get OpenStreetMap graph
#         place_name = "New York, USA"
#         graph = ox.graph_from_place(place_name, network_type='all')

#         # Get nearest nodes
#         start_node = ox.distance.nearest_nodes(graph, X=start_lon, Y=start_lat)
#         end_node = ox.distance.nearest_nodes(graph, X=end_lon, Y=end_lat)

#         # Find the shortest route
#         route = nx.shortest_path(graph, start_node, end_node, weight='length')

#         # Generate map with route
#         route_map = folium.Map(location=[start_lat, start_lon], zoom_start=12, tiles="cartodbpositron")
#         folium.PolyLine(
#             [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route],
#             color="blue", weight=5
#         ).add_to(route_map)

#         # Mark start and end
#         folium.Marker([start_lat, start_lon], popup="Start (Your Location)", icon=folium.Icon(color="green")).add_to(route_map)
#         folium.Marker([end_lat, end_lon], popup=destination, icon=folium.Icon(color="red")).add_to(route_map)

#         # Render the map dynamically
#         update_map(route_map)
#     else:
#         messagebox.showerror("Error", "Destination not found!")

# # Function to update the map dynamically in Tkinter
# def update_map(folium_map):
#     map_html = io.StringIO()
#     sys.stdout = map_html  # Redirect output to the string buffer
#     folium_map.get_root().render()
#     sys.stdout = sys.__stdout__  # Restore standard output
#     map_frame.load_html(map_html.getvalue())  # Load HTML content directly

# # Tkinter GUI Setup
# root = tk.Tk()
# root.title("Google Maps Alternative")
# root.geometry("800x600")

# # Input Field
# tk.Label(root, text="Enter Destination:").pack(pady=5)
# entry = tk.Entry(root, width=40)
# entry.pack(pady=5)

# # Buttons
# tk.Button(root, text="Show Location", command=lambda: show_map(entry.get())).pack(pady=5)
# tk.Button(root, text="Get Directions", command=lambda: find_directions(entry.get())).pack(pady=5)

# # Frame for Map Display
# map_frame = HtmlFrame(root, width=750, height=500)
# map_frame.pack(pady=10)

# # Load Initial Map (Fallback to a basic map if no current location)
# current_location = get_current_location()
# if current_location:
#     lat, lon = current_location
#     initial_map = folium.Map(location=[lat, lon], zoom_start=12, tiles="cartodbpositron")
#     update_map(initial_map)

# root.mainloop()



import folium
import osmnx as ox
import networkx as nx
import tkinter as tk
from tkinter import messagebox
from tkinterweb import HtmlFrame  # For displaying map inside Tkinter
from geopy.geocoders import Nominatim
import requests
import io
import sys

# Initialize geolocator
geolocator = Nominatim(user_agent="my_map_app")

# Function to get current location using IP
def get_current_location():
    try:
        response = requests.get("https://ipinfo.io/json").json()
        lat, lon = map(float, response["loc"].split(","))
        return lat, lon
    except:
        return None

# Function to create and display a location on the map
def show_location():
    address = entry.get()
    if not address:
        messagebox.showerror("Error", "Please enter a location.")
        return
    
    location = geolocator.geocode(address)
    if location:
        lat, lon = location.latitude, location.longitude
        my_map = folium.Map(location=[lat, lon], zoom_start=15, tiles="cartodbpositron")

        # Add marker
        folium.Marker([lat, lon], popup=location.address, icon=folium.Icon(color="blue")).add_to(my_map)

        # Update the displayed map
        update_map(my_map)
    else:
        messagebox.showerror("Error", "Location not found!")

# Function to find directions from current location
def show_directions():
    destination = entry.get()
    if not destination:
        messagebox.showerror("Error", "Please enter a destination.")
        return

    current_location = get_current_location()
    if not current_location:
        messagebox.showerror("Error", "Could not fetch current location!")
        return

    start_lat, start_lon = current_location
    location = geolocator.geocode(destination)
    
    if location:
        end_lat, end_lon = location.latitude, location.longitude

        # Get OpenStreetMap graph
        graph = ox.graph_from_point((start_lat, start_lon), dist=5000, network_type='walk')

        # Get nearest nodes
        start_node = ox.distance.nearest_nodes(graph, X=start_lon, Y=start_lat)
        end_node = ox.distance.nearest_nodes(graph, X=end_lon, Y=end_lat)

        # Find the shortest route
        route = nx.shortest_path(graph, start_node, end_node, weight='length')

        # Generate map with route
        route_map = folium.Map(location=[start_lat, start_lon], zoom_start=14, tiles="cartodbpositron")
        folium.PolyLine(
            [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route],
            color="blue", weight=5
        ).add_to(route_map)

        # Mark start and end
        folium.Marker([start_lat, start_lon], popup="Start (Your Location)", icon=folium.Icon(color="green")).add_to(route_map)
        folium.Marker([end_lat, end_lon], popup=destination, icon=folium.Icon(color="red")).add_to(route_map)

        # Update the displayed map
        update_map(route_map)
    else:
        messagebox.showerror("Error", "Destination not found!")

# Function to update the map dynamically in Tkinter
def update_map(folium_map):
    map_html = io.StringIO()
    sys.stdout = map_html  # Redirect output to the string buffer
    folium_map.get_root().render()
    sys.stdout = sys.__stdout__  # Restore standard output
    map_frame.load_html(map_html.getvalue())  # Load HTML content directly

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
tk.Button(root, text="Get Directions", command=show_directions).pack(pady=5)

# Frame for Map Display
map_frame = HtmlFrame(root, width=750, height=500)
map_frame.pack(pady=10)

# Load Initial Map
current_location = get_current_location()
if current_location:
    lat, lon = current_location
    initial_map = folium.Map(location=[lat, lon], zoom_start=12, tiles="cartodbpositron")
    update_map(initial_map)

root.mainloop()
