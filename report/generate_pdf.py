"""
This script's purpose is to generate a daily report that will be outputted as a 
PDF and send it to anyone that is a part of the subscriber list in the RDS used
for the data obtained from Bandcamp.
"""


from os import environ as ENV
from psycopg2 import connect
from dotenv import load_dotenv
from queries import (get_top_5_artists_world_sales, get_top_5_genres_world_sales, get_top_5_tracks_world_sales,
                     get_top_5_countries_sales, get_top_5_artists_volume_specific,
                     get_top_5_genres_volume_specific, get_top_5_tracks_volume_specific)


def get_connection() -> object:
    conn = connect(
        host=ENV["DB_ENDPOINT"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"],
        database=ENV["DB_NAME"],
        port=ENV["DB_PORT"]
    )

    return conn


def get_cursor(conn: object) -> object:
    cur = conn.cursor()
    return cur


def get_top_5_metrics_in_top_5_countries(cur: object, countries: list[tuple]) -> list[list]:
    countries_list = [c[0] for c in countries]
    country_metrics = []
    for country in countries_list:
        country_info = []
        country_info.append(country)
        country_info.append(get_top_5_artists_volume_specific(cur, country))
        country_info.append(get_top_5_genres_volume_specific(cur, country))
        country_info.append(get_top_5_tracks_volume_specific(cur, country))
        country_metrics.append(country_info)

    return country_metrics


if __name__ == "__main__":
    load_dotenv()
    connection = get_connection()
    cursor = get_cursor(connection)
    top_5_artists = get_top_5_artists_world_sales(cursor)
    top_5_genres = get_top_5_genres_world_sales(cursor)
    top_5_tracks = get_top_5_tracks_world_sales(cursor)
    top_5_countries = get_top_5_countries_sales(cursor)
    top_5_country_metrics = get_top_5_metrics_in_top_5_countries(
        cursor, top_5_countries)
