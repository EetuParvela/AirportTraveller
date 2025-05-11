import os
import requests
from contextlib import contextmanager
import mysql.connector
from geopy.distance import geodesic
from api import game_instance
import game


@contextmanager
def get_db_connection():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='flight_game',
        user='eetu',
        password='mdb21',
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
    target_coords = (target_coords[0], target_coords[1])
    current_coords = (current[0], current[1])
    distance = geodesic(current_coords, target_coords).kilometers
    return distance


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
                       cw.welcome_phrase
                FROM eu_airports a
                         INNER JOIN country c ON c.iso_country = a.iso_country
                         LEFT JOIN country_welcome cw ON cw.iso_country = a.iso_country
                WHERE a.ident = %s
                """, (icao,)
            )

            airport_data = cursor.fetchone()

        return {
            "country_name": airport_data['country_name'],
            "airport_name": airport_data['airport_name'],
            "latitude_deg": airport_data['latitude_deg'],
            "longitude_deg": airport_data['longitude_deg'],
            "welcome_phrase": airport_data['welcome_phrase']
        }


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
                                  cw.welcome_phrase
                           FROM eu_airports a
                                    JOIN country c ON a.iso_country = c.iso_country
                                    LEFT JOIN country_welcome cw ON a.iso_country = cw.iso_country
                           """)
            airport_data = cursor.fetchall()

            airports = []
            for row in airport_data:
                airports.append({
                    "icao": row['ident'],
                    "country_name": row['country_name'],
                    "airport_name": row['airport_name'],
                    "latitude_deg": row['latitude_deg'],
                    "longitude_deg": row['longitude_deg'],
                    "welcome_phrase": row['welcome_phrase'],
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
                                  cw.welcome_phrase
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


def get_highscore():
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cursor:
            query = "SELECT player, points FROM highscore ORDER BY points DESC LIMIT 5"
            cursor.execute(query)
            results = cursor.fetchall()
            return [{"player": row["player"], "score": row["points"]} for row in results]


def update_database(player, points):
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cursor:
            query = "INSERT INTO highscore (player, points) VALUES (%s, %s);"
            cursor.execute(query, (player, points))
        conn.commit()
