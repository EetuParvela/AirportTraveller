# Palauttaa tervehdyksen tietokannasta
def get_welcome_phrase(icao):

    with get_db_connection() as conn:
        with get_db_cursor(conn) as cursor:
            cursor.execute(f"SELECT cw.welcome_phrase "
                           f"FROM eu_airports ea "
                           f"JOIN country_welcome cw ON ea.iso_country = cw.iso_country "
                           f"WHERE ea.ident = %s ", (icao, ))
            welcome_phrase = cursor.fetchone()

            return welcome_phrase

# Hankkii käyttäjän syöttämän ICAO-koodin lentokentän tiedot tietokannasta.
def get_airport_information(code):

    sql = (f"SELECT country.name AS country_name, eu_airports.name AS airport_name, "
           f"eu_airports.latitude_deg, eu_airports.longitude_deg, eu_airports.type "
           f"FROM eu_airports "
           f"INNER JOIN country ON country.iso_country = eu_airports.iso_country "
           f"WHERE eu_airports.ident = %s ")

    with get_db_connection() as conn:
        with get_db_cursor(conn) as cursor:
            cursor.execute(sql, (code,))
            airport = cursor.fetchone()
            return airport