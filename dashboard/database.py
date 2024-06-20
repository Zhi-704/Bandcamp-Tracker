"""Functions for interacting with the database."""

from os import environ as ENV

from psycopg import connect, Connection
from psycopg.rows import dict_row
from dotenv import load_dotenv
import streamlit as st
import pandas as pd


@st.cache_resource
def get_connection() -> Connection:
    """gets a connection"""
    return connect(
        port=ENV["DB_PORT"],
        dbname=ENV["DB_NAME"],
        host=ENV["DB_ENDPOINT"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"],
        row_factory=dict_row
    )


@st.cache_data(ttl="1hr")
def get_popular_tracks(_conn: Connection, n: int = 5) -> pd.DataFrame:
    """Returns the N most sold tracks in the database."""

    print("Collating most popular tracks...")

    query = """
        SELECT T.title, A.name, COUNT(*) AS copies_sold
        FROM track_purchase AS PT
        JOIN track AS T
        USING(track_id)
        JOIN artist as A
        USING(artist_id)
        GROUP BY T.title, A.name
        ORDER BY copies_sold DESC
        LIMIT %s
        ;
        """

    with _conn.cursor() as cur:
        cur.execute(query, (n,))
        data = cur.fetchall()

    return pd.DataFrame(data)


@st.cache_data(ttl="1hr")
def get_popular_albums(_conn: Connection, n: int = 5) -> pd.DataFrame:
    """Returns the N most sold albums in the database."""

    print("Collating most popular albums...")

    query = """
        SELECT AB.title, AT.name, COUNT(*) AS copies_sold
        FROM album_purchase AS PA
        JOIN album AS AB
        USING(album_id)
        JOIN artist as AT
        USING(artist_id)
        GROUP BY AB.title, AT.name
        ORDER BY copies_sold DESC
        LIMIT %s
        ;
        """

    with _conn.cursor() as cur:
        cur.execute(query, (n,))
        data = cur.fetchall()

    return pd.DataFrame(data)


@st.cache_data(ttl="1hr")
def get_popular_artists(_conn: Connection, n: int = 5) -> pd.DataFrame:
    """Returns the N artists with the most sales in the database."""

    print("Collating most popular artists...")

    query = """
        SELECT A.name, COUNT(AP.album_purchase_id) AS album_sales, COUNT(TP.track_purchase_id) AS track_sales, COUNT(AP.album_purchase_id) + COUNT(TP.track_purchase_id) AS total_sales
        FROM artist as A
        JOIN album AS AB
        USING(artist_id)
        JOIN album_purchase AS AP
        USING(album_id)
        JOIN track as T
        USING(artist_id)
        JOIN track_purchase as TP
        USING(track_id)
        GROUP BY AB.title, A.name
        ORDER BY total_sales DESC
        LIMIT %s
        ;
        """

    with _conn.cursor() as cur:
        cur.execute(query, (n,))
        data = cur.fetchall()

    return pd.DataFrame(data)


@st.cache_data(ttl="1hr")
def get_sales_by_tag(_conn: Connection, n: int = 5) -> pd.DataFrame:
    """Returns the top n genre/tag by sales."""

    print("Counting sales by tag...")

    query = """
        SELECT TG.name AS tag, COUNT(*) AS total_sales
        FROM tag AS TG
        JOIN album_tag_assignment AS ATG
        ON ATG.tag_id =TG.tag_id
        JOIN track_tag_assignment AS TGA
        ON TGA.tag_id = TG.tag_id
        JOIN album AS A
        USING(album_id)
        JOIN track AS T
        USING(track_id)
        JOIN album_purchase AS AP
        ON AP.album_id = A.album_id
        JOIN track_purchase AS TP
        ON TP.track_id = T.track_id
        GROUP BY tag
        ORDER BY total_sales DESC
        LIMIT %s
        ;
        """

    with _conn.cursor() as cur:
        cur.execute(query, (n, ))
        data = cur.fetchall()

    return pd.DataFrame(data)


@st.cache_data(ttl="1hr")
def get_all_tags(_conn: Connection) -> list:
    """Returns all tags."""

    print("Collecting tags...")

    query = """
        SELECT name
        FROM tag
        ;
        """

    with _conn.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()
    return sorted([d["name"] for d in data])


def get_sales_by_country(_conn: Connection, n: int = 5):
    """Returns the top n countries by sales."""

    print("Counting sales by country...")

    query = """
        SELECT C.name, COUNT(album_purchase_id)+COUNT(track_purchase_id) AS total_sales
        FROM country AS C
        JOIN album_purchase AS AP
        USING(country_id)
        JOIN track_purchase AS TP
        ON TP.country_id = C.country_id
        GROUP BY C.name
        ORDER BY total_sales DESC
        LIMIT %s
        ;
        """

    with _conn.cursor() as cur:
        cur.execute(query, (n, ))
        data = cur.fetchall()

    return data
