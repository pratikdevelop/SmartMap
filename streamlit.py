import folium
import streamlit as st
from geopy.geocoders import Nominatim
import streamlit.components.v1 as components

# Initialize geolocator
geolocator = Nominatim(user_agent="my_map_app")

# Function to get address from latitude and longitude
def get_address_from_coordinates(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language="en")
        return location.address if location else "Address not found"
    except Exception as e:
        st.error(f"Error retrieving address: {e}")
        return None

# Function to show the current location on the map
def show_current_location_on_map(lat, lon, address):
    my_map = folium.Map(location=[lat, lon], zoom_start=15, tiles="cartodbpositron")
    
    # Add a marker with the address
    folium.Marker([lat, lon], popup=address, icon=folium.Icon(color="blue")).add_to(my_map)
    
    # Render the map
    map_html = my_map._repr_html_()
    components.html(map_html, height=500)

# Function to display the browser's geolocation using JavaScript
def get_browser_geolocation():
    geolocation_script = """
    <script type="text/javascript">
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            console.log("Latitude: " + lat + ", Longitude: " + lon);  // Debugging log
            // Pass the lat and lon to Streamlit using window.parent
            window.parent.postMessage({ lat: lat, lon: lon }, "*");
        }, function(error) {
            console.log("Geolocation Error: " + error.message);  // Debugging log for errors
            alert("Error: " + error.message);  // Display error message in the browser
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
    </script>
    """
    components.html(geolocation_script, height=0)  # We don't need to display this component

# Main Streamlit app
def main():
    st.title("Google Maps Alternative - Current Location via Browser")

    # Display a message to the user
    st.write("Please allow your browser to access your location.")

    # Fetch browser geolocation
    get_browser_geolocation()

    # Listen for the coordinates from the JavaScript message
    if 'lat' in st.session_state and 'lon' in st.session_state:
        lat = st.session_state.lat
        lon = st.session_state.lon
        st.write(f"Current Coordinates: Latitude = {lat}, Longitude = {lon}")
        
        # Get address from current location
        address = get_address_from_coordinates(lat, lon)
        if address:
            st.write(f"Current Location Address: {address}")

            # Display the current location on the map
            show_current_location_on_map(lat, lon, address)
        else:
            st.error("Could not retrieve the address for your current location.")
    else:
        st.warning("Waiting for geolocation...")

# Listen for messages from the JS code to update session state
@st.cache_data
def update_session_state(msg):
    if 'lat' in msg and 'lon' in msg:
        st.session_state.lat = msg['lat']
        st.session_state.lon = msg['lon']

if __name__ == "__main__":
    main()


# import folium
# from geopy.geocoders import Nominatim

# # Initialize geolocator
# geolocator = Nominatim(user_agent="my_map_app")

# # Function to get address from latitude and longitude
# def get_address_from_coordinates(lat, lon):
#     try:
#         location = geolocator.reverse((lat, lon), language="en")
#         return location.address if location else "Address not found"
#     except Exception as e:
#         return f"Error retrieving address: {e}"

# # Function to generate a Folium map HTML
# def generate_map(lat, lon, address):
#     # Create the map centered at the coordinates
#     my_map = folium.Map(location=[lat, lon], zoom_start=15, tiles="cartodbpositron")
    
#     # Add a marker with the address
#     folium.Marker([lat, lon], popup=address, icon=folium.Icon(color="blue")).add_to(my_map)
    
#     # Generate the HTML representation of the map
#     return my_map._repr_html_()

# # Example coordinates
# lat = 23.1735296  # Replace with dynamic coordinates if needed
# lon = 75.7956608  # Replace with dynamic coordinates if needed

# # Get address for the current location
# address = get_address_from_coordinates(lat, lon)

# # Generate the map HTML
# map_html = generate_map(lat, lon, address)

# # Save the HTML to a file (or you can use it directly in a web server)
# with open("map.html", "w") as file:
#     file.write(map_html)

# print("Map HTML file generated!")