"""
This script's purpose is to generate a daily report that will be outputted as a
PDF and then to send it to anyone that is a part of the subscriber list in the RDS
that is used to store the data which is extracted from Bandcamp.
"""


from os import environ as ENV
from io import BytesIO
from base64 import b64encode
from psycopg2 import connect
from dotenv import load_dotenv
import altair as alt
from xhtml2pdf import pisa
from tabulate import tabulate
from queries import (get_top_5_artists_world_sales,
                     get_top_5_tags_world_sales,
                     get_top_5_tracks_world_sales,
                     get_top_5_countries_sales,
                     get_top_5_metrics_in_top_5_countries)
from charts import (get_top_artists_chart,
                    get_top_tags_chart,
                    get_top_tracks_chart)


def get_connection() -> object:
    """This function uses psycopg2 to create the connection to the RDS"""
    conn = connect(
        host=ENV["DB_ENDPOINT"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"],
        database=ENV["DB_NAME"],
        port=ENV["DB_PORT"]
    )

    return conn


def get_cursor(conn: object) -> object:
    """This function uses the connection object to create a cursor object"""
    cur = conn.cursor()
    return cur


def get_top_5_countries(countries: list[tuple]) -> list[str]:
    """
    This function iterates through the list of tuples to output
    a new list that contains the just the country name in descending order
    which is ranked off of performance by total revenue made.
    """
    list_of_countries = [c[0] for c in countries]
    return list_of_countries


def convert_html_to_pdf(source_html: str, output_filename: str) -> None:
    """Outputs HTML to a target file and stores it as a PDF."""
    with open(output_filename, "w+b") as f:
        pisa_status = pisa.CreatePDF(source_html, dest=f)

    return pisa_status


def create_html_tables(countries: list[str], country_infos: list[list]) -> str:
    """
    This function takes a list of countries and all their metrics and puts them
    a table in the form of a HTML script.
    """
    tables = ""
    headers = ["Artists", "Tracks", "Tags"]

    for i, country in enumerate(countries):
        country_table = tabulate(
            list(zip(*country_infos[i])), headers=headers, tablefmt="html")
        tables += f"""
    <table>
        <caption> {country} </caption>
        {country_table[7:]}
    </table>"""

    return tables


def create_html_chart(chart: alt.Chart) -> str:
    """This function takes in altair charts and converts them into HTML """
    with BytesIO() as bs:
        chart.save(bs, format="png")
        bs.seek(0)

        data = b64encode(bs.read()).decode("utf-8")

    return f"data:image/png;base64,{data}"


if __name__ == "__main__":
    load_dotenv()

    connection = get_connection()
    cursor = get_cursor(connection)

    top_5_artists = get_top_5_artists_world_sales(cursor)
    top_5_tags = get_top_5_tags_world_sales(cursor)
    top_5_tracks = get_top_5_tracks_world_sales(cursor)

    artists_chart = get_top_artists_chart(top_5_artists)
    artists_chart_html = create_html_chart(artists_chart)
    tags_chart = get_top_tags_chart(top_5_tags)
    tags_chart_html = create_html_chart(tags_chart)
    tracks_chart = get_top_tracks_chart(top_5_tracks)
    tracks_chart_html = create_html_chart(tracks_chart)

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
    <link rel="stylesheet" type="text/css" href="{ENV['CSS_PATH']}" />
</head>
<body>
    <h1>Bandcamp Daily Report</h1>
    <h2>Good Morning Subscriber!<br>Today's daily report provides information on worldwide trends and country specific ones too.</h2>
    <h3><br>Top 5 Rankings Worldwide by Total Revenue</h3>
    <div class="charts">
        <img src="{artists_chart_html}" class="responsive-charts" style="float:left;"/>
        <img src="{tracks_chart_html}" class="responsive-charts" style="float:right;" />
        <img src="{tags_chart_html}" class="responsive-charts" />
    </div>
    <h3><br>Top 5 Rankings based on Location by Number of Purchases </3>
    {html_tables}
</body>
</html>
"""

    convert_result = convert_html_to_pdf(html_report, ENV["FILENAME"])
