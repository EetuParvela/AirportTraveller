from contextlib import contextmanager
import mysql.connector
from geopy.distance import geodesic


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

# Palauttaa lentokentän tiedot
def get_airport_info(icao):
    airport_data = None
    welcome_phrase = None

    with get_db_connection() as conn:
        with get_db_cursor(conn) as cursor:

            # Hakee lentokentän tiedot
            cursor.execute(
                """
                SELECT country.name AS country_name,
                       eu_airports.name AS airport_name,
                       eu_airports.latitude_deg,
                       eu_airports.longitude_deg
                FROM eu_airports
                INNER JOIN country ON country.iso_country = eu_airports.iso_country
                WHERE eu_airports.ident = %s
                """, (icao,))
            airport_data = cursor.fetchone()

            # Hakee tervehdyksen
            cursor.execute(
                """
                SELECT cw.welcome_phrase
                FROM eu_airports ea
                JOIN country_welcome cw ON ea.iso_country = cw.iso_country
                WHERE ea.ident = %s
                """, (icao,))
            result = cursor.fetchone()
            welcome_phrase = result['welcome_phrase'] if result else None

    if airport_data:
        return {
            "country_name": airport_data['country_name'],
            "airport_name": airport_data['airport_name'],
            "latitude_deg": airport_data['latitude_deg'],
            "longitude_deg": airport_data['longitude_deg'],
            "welcome_phrase": welcome_phrase
        }
    else:
        return None


# Palauttaa 5 lähintä lentokenttää pelaajaan
def get_closest_airports(current_icao):

    with get_db_connection() as conn:
        with get_db_cursor(conn) as cursor:

            # Hakee nykyisen lentokentän tiedot
            cursor.execute("SELECT latitude_deg, longitude_deg FROM eu_airports WHERE ident = %s", (current_icao,))
            current = cursor.fetchone()

            current_coords = (current['latitude_deg'], current['longitude_deg'])

            # Hakee kaikki lentokentät tietokannasta
            cursor.execute("""
                SELECT a.ident, a.name AS airport_name, a.latitude_deg, a.longitude_deg, c.name AS country_name
                FROM eu_airports a
                JOIN country c ON a.iso_country = c.iso_country
                WHERE a.ident != %s
            """, (current_icao,))
            airports = cursor.fetchall()

            # Laskee kenttien välisen matkan
            for airport in airports:
                target_coords = (airport['latitude_deg'], airport['longitude_deg'])
                airport['distance_km'] = geodesic(current_coords, target_coords).kilometers

            # Järjestää ja palauttaa 5 lähintä lentokenttää
            airports.sort(key=lambda x: x['distance_km'])
            return airports[:5]

# Palauttaa kaikki lentokentät tietokannasta
def get_all_airports():

    with get_db_connection() as conn:
        with get_db_cursor(conn) as cursor:

            cursor.execute("""
                SELECT a.ident, a.name AS airport_name, a.latitude_deg, a.longitude_deg, c.name AS country_name
                FROM eu_airports a
                JOIN country c ON a.iso_country = c.iso_country
                """)
            airports = cursor.fetchall()
            return airports
