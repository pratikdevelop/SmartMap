import folium
import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Initialize geolocator
geolocator = Nominatim(user_agent="SmartMap")

# Function to get the current location using IP
def get_current_location():
    try:
        response = requests.get("https://ipinfo.io/json").json()
        lat, lon = map(float, response["loc"].split(","))
        return lat, lon
    except Exception as e:
        print(f"Error retrieving current location: {e}")
        return None

# Function to get address from latitude and longitude
def get_address_from_coordinates(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language="en")
        return location.address if location else "Address not found"
    except Exception as e:
        return f"Error retrieving address: {e}"

# Function to create and display a location on the map
def generate_map(lat, lon, address):
    # Create the map centered at the coordinates
    my_map = folium.Map(location=[lat, lon], zoom_start=15, tiles="cartodbpositron")
    
    # Add a marker with the address
    folium.Marker([lat, lon], popup=address, icon=folium.Icon(color="blue")).add_to(my_map)
    
    # Save the map to an HTML file
    map_path = os.path.join(os.getcwd(), "map.html")
    my_map.save(map_path)
    
    return map_path

# Function to get the route between two locations using OSMnx
def get_route(start_lat, start_lon, end_lat, end_lon):
    # Load the street network for a given location
    G = ox.graph_from_place("Chicago, Illinois", network_type="all")
    
    # Get the nearest network nodes to the start and end points
    start_node = ox.distance.nearest_nodes(G, X=start_lon, Y=start_lat)
    end_node = ox.distance.nearest_nodes(G, X=end_lon, Y=end_lat)
    
    # Get the shortest path between the start and end nodes
    route = nx.shortest_path(G, start_node, end_node, weight="length")
    
    # Get the route's latitude and longitude coordinates
    route_lat_lon = [(G.nodes[node]["y"], G.nodes[node]["x"]) for node in route]
    
    # Create a map with the route
    route_map = folium.Map(location=[start_lat, start_lon], zoom_start=15, tiles="cartodbpositron")
    folium.Marker([start_lat, start_lon], popup="Start", icon=folium.Icon(color="green")).add_to(route_map)
    folium.Marker([end_lat, end_lon], popup="End", icon=folium.Icon(color="red")).add_to(route_map)
    
    # Add the route to the map
    folium.PolyLine(route_lat_lon, color="blue", weight=3, opacity=0.7).add_to(route_map)
    
    # Save the route map to an HTML file
    route_map_path = "static/map.html"
    route_map.save(route_map_path)
    
    return route_map_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_location', methods=['POST'])
def get_location():
    lat = request.json.get('lat')
    lon = request.json.get('lon')
    
    # Get the address from coordinates
    address = get_address_from_coordinates(lat, lon)
    
    # Generate the map with the address and coordinates
    map_html_path = generate_map(lat, lon, address)
    
    return jsonify({'map_html': map_html_path, 'address': address})



# Function to get the route between two locations using OSMnx
def get_route(start_lat, start_lon, end_lat, end_lon):
    # Load the street network for a given location
    G = ox.graph_from_place("Chicago, Illinois", network_type="all")
    
    # Get the nearest network nodes to the start and end points
    start_node = ox.distance.nearest_nodes(G, X=start_lon, Y=start_lat)
    end_node = ox.distance.nearest_nodes(G, X=end_lon, Y=end_lat)
    
    # Get the shortest path between the start and end nodes
    route = nx.shortest_path(G, start_node, end_node, weight="length")
    
    # Get the route's latitude and longitude coordinates
    route_lat_lon = [(G.nodes[node]["y"], G.nodes[node]["x"]) for node in route]
    
    # Create a map with the route
    route_map = folium.Map(location=[start_lat, start_lon], zoom_start=15, tiles="cartodbpositron")
    folium.Marker([start_lat, start_lon], popup="Start", icon=folium.Icon(color="green")).add_to(route_map)
    folium.Marker([end_lat, end_lon], popup="End", icon=folium.Icon(color="red")).add_to(route_map)
    
    # Add the route to the map
    folium.PolyLine(route_lat_lon, color="blue", weight=3, opacity=0.7).add_to(route_map)
    
    # Save the route map to an HTML file
    route_map_path = "static/map.html"
    route_map.save(route_map_path)
    
    return route_map_path

# Flask route to handle the POST request for route generation
@app.route('/get_route', methods=['POST'])
def get_route_api():
    try:
        # Get the coordinates from the request
        data = request.get_json()
        start_lat = data.get('start_lat')
        start_lon = data.get('start_lon')
        end_lat = data.get('end_lat')
        end_lon = data.get('end_lon')
        
        # Check if the coordinates are provided
        if not all([start_lat, start_lon, end_lat, end_lon]):
            return jsonify({'error': 'Missing coordinates'}), 400
        
        # Get the route map
        route_map_path = get_route(start_lat, start_lon, end_lat, end_lon)
        
        return jsonify({'route_map_html': route_map_path})
    
    except Exception as e:
        return jsonify({'error': f'Error generating route: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
