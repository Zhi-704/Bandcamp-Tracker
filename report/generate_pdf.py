"""
This script's purpose is to generate a daily report that will be outputted as a 
PDF and send it to anyone that is a part of the subscriber list in the RDS used
for the data obtained from Bandcamp.
"""


from os import environ as ENV
from psycopg2 import connect
from dotenv import load_dotenv
from xhtml2pdf import pisa
from tabulate import tabulate
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
    country_metrics = []
    for country in countries:
        country_info = []
        country_info.append(get_top_5_artists_volume_specific(cur, country))
        country_info.append(get_top_5_genres_volume_specific(cur, country))
        country_info.append(get_top_5_tracks_volume_specific(cur, country))
        country_metrics.append(country_info)

    return country_metrics


def get_top_5_countries(countries: list[tuple]) -> list[str]:
    list_of_countries = [c[0] for c in countries]
    return list_of_countries


def convert_html_to_pdf(source_html, output_filename):
    """Outputs HTML to a target file."""
    with open(output_filename, "w+b") as f:
        pisa_status = pisa.CreatePDF(source_html, dest=f)


if __name__ == "__main__":
    load_dotenv()
    connection = get_connection()
    cursor = get_cursor(connection)

    top_5_artists = get_top_5_artists_world_sales(cursor)
    top_5_genres = get_top_5_genres_world_sales(cursor)
    top_5_tracks = get_top_5_tracks_world_sales(cursor)
    top_5_countries = get_top_5_countries_sales(cursor)
    countries_list = get_top_5_countries(top_5_countries)
    top_5_country_metrics = get_top_5_metrics_in_top_5_countries(
        cursor, countries_list)

    cursor.close()
    connection.close()

    headers = ["Top 5 Artists", "Top 5 Tags", "Top 5 Tracks"]
    country1_table = tabulate(
        list(zip(*top_5_country_metrics[0])), headers=headers, tablefmt="html")

    html_report = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        h1 {{ text-align: center; }}
        table, th, td {{ border: none; border-collapse: collapse; padding: 2px; text-align: center; }}
        table {{ width: 100%; margin: 5px 0; }}
        th {{ background-color: #f2f2f2; }}
        caption {{ border: none; text-align: center; font-size: 1.5em; font-weight: bold; margin-top: 0px; margin-bottom: 0px; }}
    </style>
</head>
<body>
    <h1>Bandcamp Daily Report:</h1>
    <p style="text-align: center;">Good morning subscriber! Here is today's daily report on Bandcamp metrics both worldwide and for specific countries.</p>
    <table>
        <caption>{countries_list[0]}</caption>
        {country1_table[7:]}
    </table>
</body>
</html>
"""

    convert_html_to_pdf(html_report, ENV["FILENAME"])
