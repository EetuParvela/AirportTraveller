import os
import requests
from geopy.distance import geodesic
from dotenv import load_dotenv
from database import get_all_airports


def airport_infos():
    airports = get_all_airports()
    airport_data_list = []
    for airport in airports:
        weather = get_weather_data(airport["latitude_deg"], airport["longitude_deg"])
        airport_info = {
            "icao": airport["ident"],
            "name": airport["airport_name"],
            "country_name": airport["country_name"],
            "lat": airport["latitude_deg"],
            "lon": airport["longitude_deg"],
        }
        airport_data_list.append(airport_info)

    return airport_data_list

def get_weather_data(lat, lon):
    load_dotenv()
    api_key = os.getenv("api_key")
    request = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    answer = requests.get(request)
    weather_data = answer.json()
    return weather_data

def calculate_distance(current_coords, target_coords):
    target_coords = (target_coords['latitude_deg'], target_coords['longitude_deg'])
    distance = geodesic(current_coords, target_coords).kilometers
    return distance
