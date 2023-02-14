from flask import Flask, request
import plotly.express as px
import pandas as pd
from geopy.geocoders import Nominatim
import random

app = Flask(__name__)

@app.route("/")
def index():
    return '''
        <form method="post">
            City Name: <input type="text" name="city_name"><br>
            <input type="submit" value="Submit">
        </form>
    '''

@app.route("/", methods=["POST"])
def generate_map():
    # Set Mapbox access token
    px.set_mapbox_access_token('pk.eyJ1Ijoic2h5YW0xOTA5IiwiYSI6ImNsZGsxeXh5cTAyOWQ0MG8zbXlqejF1OHAifQ.SYCrE9VXwIxHf6zAYv4VxA')

    # Get the city name from the form data
    city_name = request.form["city_name"]

    # Use the geopy library to get the latitude and longitude of the city
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city_name)
    latitude = location.latitude
    longitude = location.longitude

    # Generate random data for demonstration purposes
    df = pd.DataFrame({
        "latitude": [latitude + random.uniform(-0.03, 0.03) for i in range(100)],
        "longitude": [longitude + random.uniform(-0.03, 0.03) for i in range(100)],
        "speed": [20 + random.uniform(-10, 30) for i in range(100)],
        "vehicle_id": [f"vehicle_{i}" for i in range(100)],
    })

    # Create a scatter mapbox plot of the data
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", size="speed", color="speed", animation_frame="vehicle_id",
                      color_continuous_scale=px.colors.sequential.Plasma, size_max=15, zoom=10,
                      center=dict(lat=latitude, lon=longitude))

    return fig.to_html()

    # make sure that the points are not plotted randomly and they are plotted only on roads
    # use google maps api to get the latitude and longitude coordinates of streets in chennai

    

if __name__ == "__main__":
    app.run()
