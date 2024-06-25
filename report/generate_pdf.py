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
                     get_top_5_countries_sales, get_top_5_metrics_in_top_5_countries)


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


def get_top_5_countries(countries: list[tuple]) -> list[str]:
    list_of_countries = [c[0] for c in countries]
    return list_of_countries


def convert_html_to_pdf(source_html: str, output_filename: str) -> None:
    """Outputs HTML to a target file."""
    with open(output_filename, "w+b") as f:
        pisa_status = pisa.CreatePDF(source_html, dest=f)


def create_html_tables(countries: list[str], country_infos: list[list]):
    tables = ""
    headers = ["Top 5 Artists", "Top 5 Tags", "Top 5 Tracks"]

    for i, country in enumerate(countries):
        country_table = tabulate(
            list(zip(*country_infos[i])), headers=headers, tablefmt="html")
        tables += f"""
    <table>
        <caption> {country} </caption>
        {country_table[7:]}  <!-- Stripping the <table> tag from tabulate output -->
    </table>"""

    return tables


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

    html_tables = create_html_tables(countries_list, top_5_country_metrics)

    html_report = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        h1 {{ text-align: center; }}
        table, th, td {{ border: none; border-collapse: collapse; padding: 2px; }}
        table {{ width: 100%; margin: 5px; }}
        th {{ background-color: #f2f2f2; vertical-align: center }}
        td {{ vertical-align: top; text-align: center;}}
        caption {{ border: none; text-align: center; font-size: 1.5em; font-weight: bold; margin-top: 0px; margin-bottom: 0px; }}
    </style>
</head>
<body>
    <h1>Bandcamp Daily Report:</h1>
    <p style="text-align: center;">Good morning subscriber! Here is today's daily report on Bandcamp metrics both worldwide and for specific countries.</p>
    {html_tables}
</body>
</html>
"""

    convert_html_to_pdf(html_report, ENV["FILENAME"])
