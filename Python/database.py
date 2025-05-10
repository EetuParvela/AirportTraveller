import os
import requests
from contextlib import contextmanager
import mysql.connector
from geopy.distance import geodesic


@contextmanager
def get_db_connection():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='flight_game',
        user='lauri1',
        password='salis1',
        charset="utf8mb4",
        collation="utf8mb4_general_ci",
        autocommit=True
    )
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def get_db_cursor(conn):
    cursor = conn.cursor(dictionary=True)
    try:
        yield cursor
    finally:
        cursor.close()


def calculate_distance(current, target_coords):
    target_coords = (target_coords['latitude_deg'], target_coords['longitude_deg'])
    current_coords = (current["latitude_deg"], current["longitude_deg"])
    distance = geodesic(current_coords, target_coords).kilometers
    return distance


def get_weather(lat, lon):
    api_key = os.getenv("API_KEY")  # Suositellaan käytettäväksi ympäristömuuttujia
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    return {
        "main": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
        "temp": data["main"]["temp"]
    }


# Hankkii yhden lentokentän tiedot tietokannasta
def get_airport_info(icao):
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                """
                SELECT c.name AS country_name,
                       a.name AS airport_name,
                       a.latitude_deg,
                       a.longitude_deg,
                       cw.welcome_word
                FROM eu_airports a
                         INNER JOIN country c ON c.iso_country = a.iso_country
                         LEFT JOIN country_welcome cw ON cw.iso_country = a.iso_country
                WHERE a.ident = %s
                """, (icao,)
            )

            airport_data = cursor.fetchone()

    if airport_data:
        return {
            "country_name": airport_data['country_name'],
            "airport_name": airport_data['airport_name'],
            "latitude_deg": airport_data['latitude_deg'],
            "longitude_deg": airport_data['longitude_deg'],
            "welcome_word": airport_data['welcome_word']
        }
    else:
        return None


# Palauttaa kaikki lentokentät tietokannasta
def get_all_airports():

    with get_db_connection() as conn:
        with get_db_cursor(conn) as cursor:

            cursor.execute("""
                           SELECT a.ident,
                                  a.name AS airport_name,
                                  a.latitude_deg,
                                  a.longitude_deg,
                                  c.name AS country_name,
                                  cw.welcome_word
                           FROM eu_airports a
                            JOIN country c ON a.iso_country = c.iso_country
                            LEFT JOIN country_welcome cw ON a.iso_country = cw.iso_country
                           """)
            airport_data = cursor.fetchall()

            airports = []
            for row in airport_data:
                weather = get_weather(row['latitude_deg'], row['longitude_deg'])
                airports.append({
                    "icao": row['ident'],
                    "country_name": row['country_name'],
                    "airport_name": row['airport_name'],
                    "latitude_deg": row['latitude_deg'],
                    "longitude_deg": row['longitude_deg'],
                    "welcome_word": row['welcome_word'],
                    "weather": weather
                })

            return airports


# Palauttaa 5 lähintä lentokenttää pelaajaan
def get_closest_airports(current_icao):

    with get_db_connection() as conn:
        with get_db_cursor(conn) as cursor:

            # Hakee nykyisen lentokentän tiedot
            cursor.execute("SELECT latitude_deg, longitude_deg FROM eu_airports WHERE ident = %s", (current_icao,))
            current = cursor.fetchall()

            current_coords = (current[0]['latitude_deg'], current[0]['longitude_deg'])

            # Hakee kaikki lentokentät tietokannasta
            cursor.execute("""
                           SELECT a.ident,
                                  a.name AS airport_name,
                                  a.latitude_deg,
                                  a.longitude_deg,
                                  c.name AS country_name,
                                  cw.welcome_word
                            FROM eu_airports a
                            JOIN country c ON a.iso_country = c.iso_country
                            LEFT JOIN country_welcome cw ON a.iso_country = cw.iso_country
                           WHERE a.ident != %s
                           """, (current_icao,))
            airports = cursor.fetchall()

            # Laskee kenttien välisen matkan
            for airport in airports:
                target_coords = (airport["latitude_deg"], airport["longitude_deg"])
                airport['distance_km'] = geodesic(current_coords, target_coords).kilometers

            # Järjestää ja palauttaa 5 lähintä lentokenttää
            airports.sort(key=lambda x: x['distance_km'])
            return airports[:5]