import os
import requests
from dotenv import load_dotenv
from database import get_all_airports

def get_weather_data(lat, lon):
    load_dotenv()
    api_key = os.getenv("weather_api_key")
    request = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    answer = requests.get(request)
    weather_data = answer.json()
    return weather_data

airports = get_all_airports()

def airport_infos():
    airport_data_list = []
    for airport in airports:
        weather = get_weather_data(airport["latitude_deg"], airport["longitude_deg"])
        airport_info = {
            "icao": airport["ident"],
            "name": airport["airport_name"],
            "country_name": airport["country_name"],
            "lat": airport["latitude_deg"],
            "lon": airport["longitude_deg"],
            "weather": {
                "main": weather["weather"][0]["main"],
                "temp": weather["main"]["temp"]
            }
        }
        airport_data_list.append(airport_info)

    return airport_data_list

print(airport_infos())