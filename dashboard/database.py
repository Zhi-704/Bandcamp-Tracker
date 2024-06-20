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
        SELECT A.name, COUNT(AP.album_purchase_id)+COUNT(TP.track_purchase_id) AS total_sales
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
        LEFT JOIN album_tag_assignment AS ATG
        USING(tag_id)
        LEFT JOIN track_tag_assignment AS TGA
        USING(tag_id)
        LEFT JOIN album AS A
        USING(album_id)
        LEFT JOIN track AS T
        USING(track_id)
        LEFT JOIN album_purchase AS AP
        USING(album_id)
        LEFT JOIN track_purchase AS TP
        USING(track_id)
        GROUP BY tag
        ORDER BY total_sales DESC
        LIMIT %s
        ;
        """

    with _conn.cursor() as cur:
        cur.execute(query, (n, ))
        data = cur.fetchall()

    return pd.DataFrame(data)
