"""Script containing functions for loading sales data into the Database."""

from os import environ as ENV
import psycopg2
import psycopg2.extras
from psycopg2 import sql
from psycopg2.extensions import connection, cursor
from dotenv import load_dotenv
import logging


def get_connection() -> connection:
    """Creates a database session and returns a connection object."""
    return psycopg2.connect(
        host=ENV["DB_HOST"],
        port=ENV["DB_PORT"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASS"],
        database=ENV["DB_NAME"],
    )


def get_cursor(connection: connection) -> cursor:
    """Creates and returns a cursor to execute PostgreSQL commands."""
    return connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def get_or_insert_artist(cursor: cursor, artist_name: str, artist_url: str) -> str:
    """Adds the artist to the artist table and returns the artist_id if not present, otherwise gets the
    artist_id from the table"""

    cursor.execute(
        "SELECT artist_id FROM artist WHERE name = %s AND artist_url = %s",
        (
            artist_name,
            artist_url,
        ),
    )
    artist_id = cursor.fetchone()

    if artist_id:
        return artist_id[0]

    cursor.execute(
        "INSERT INTO artist(name, artist_url) VALUES (%s, %s) RETURNING artist_id",
        (artist_name, artist_url),
    )
    return cursor.fetchone()[0]


def get_or_insert_country(cursor: cursor, country_name: str) -> str:
    """Adds the country to the country table and returns the country_id if not present, otherwise gets the
    country_id from the table."""

    cursor.execute("SELECT country_id FROM country WHERE name = %s", (country_name,))
    country_id = cursor.fetchone()

    if country_id:
        return country_id[0]

    cursor.execute(
        "INSERT INTO country(name) VALUES (%s) RETURNING country_id", (country_name,)
    )
    return cursor.fetchone()[0]


def get_or_insert_album(
    cursor: cursor, album_title: str, artist_id: int, album_url: str
) -> str:
    """Adds the album to the album table and returns the album_id if not present, otherwise gets the
    album_id from the table."""

    cursor.execute(
        "SELECT album_id FROM album WHERE title = %s AND artist_id = %s AND album_url = %s",
        (album_title, artist_id, album_url),
    )
    album_id = cursor.fetchone()

    if album_id:
        return album_id[0]

    cursor.execute(
        "INSERT INTO album(title, artist_id, album_url) VALUES (%s, %s, %s) RETURNING album_id",
        (album_title, artist_id, album_url),
    )
    return cursor.fetchone()[0]


def get_or_insert_track_or_single(
    cursor: cursor, song_title: str, artist_id: int, song_url: str, album_id: int = -1
) -> str:
    """Adds the track to the track table and returns the track_id if not present, otherwise gets the
    track_id from the table."""

    cursor.execute(
        "SELECT track_id FROM track WHERE title = %s AND artist_id = %s AND track_url = %s",
        (song_title, artist_id, song_url),
    )
    track_id = cursor.fetchone()

    if track_id:
        return track_id[0]

    if not album_id == -1:
        cursor.execute(
            "INSERT INTO track(title, album_id, artist_id, track_url) VALUES (%s, %s, %s, %s) RETURNING track_id",
            (song_title, album_id, artist_id, song_url),
        )
        return cursor.fetchone()[0]
    elif album_id == -1:
        cursor.execute(
            "INSERT INTO track(title, artist_id, track_url) VALUES (%s, %s, %s) RETURNING track_id",
            (song_title, artist_id, song_url),
        )
        return cursor.fetchone()[0]


def get_or_insert_tags(
    cursor: cursor, tag_name: str, album_id: int = -1, track_id: int = -1
) -> None:
    """Adds the tab to the tag table, returns the tag_id, inserts row in album_tag_assignment table,
    otherwise gets the tag_id and then inserts row in assignment table."""

    cursor.execute("SELECT tag_id FROM tag WHERE name = %s", (tag_name,))
    tag_id = cursor.fetchone()

    if not tag_id:
        cursor.execute(
            "INSERT INTO tag(name) VALUES (%s) RETURNING tag_id", (tag_name,)
        )
        tag_id = cursor.fetchone()[0]

    if not album_id == -1:
        cursor.execute(
            "INSERT INTO album_tag_assignment(tag_id, album_id) VALUES (%s, %s)",
            (tag_id, album_id),
        )
    if not track_id == -1:
        cursor.execute(
            "INSERT INTO track_tag_assignment(tag_id, track_id) VALUES (%s, %s)",
            (tag_id, track_id),
        )


def insert_album_or_track_purchase(
    cursor: cursor,
    timestamp: str,
    amount_usd: int,
    country_id: int,
    album_id: int = -1,
    track_id: int = -1,
) -> None:
    """Inserts an album or track purchase in the (album/track)_purchase table."""

    if not album_id == -1:
        cursor.execute(
            "INSERT INTO album_purchase(album_id, timestamp, amount_usd, country_id) VALUES (%s, %s, %s, %s)",
            (album_id, timestamp, amount_usd, country_id),
        )
    elif not track_id == -1:
        cursor.execute(
            "INSERT INTO track_purchase(track_id, timestamp, amount_usd, country_id) VALUES (%s, %s, %s, %s)",
            (track_id, timestamp, amount_usd, country_id),
        )


def insert_album_sale(cursor: cursor, album_sale: dict) -> None:
    """Inserts data relating to an album sale."""

    country = album_sale["country"]
    country_id = get_or_insert_country(cursor, country)

    artist = album_sale["artist_name"]
    artist_url = album_sale["artist_url"]
    artist_id = get_or_insert_artist(cursor, artist, artist_url)

    album_title = album_sale["item_description"]
    album_url = album_sale["url"]
    album_id = get_or_insert_album(cursor, album_title, artist_id, album_url)

    for tag in album_sale["album_tags"]:
        get_or_insert_tags(cursor, tag, album_id)

    timestamp = album_sale["utc_date"]
    amount_usd = album_sale["amount_paid_usd"]
    insert_album_or_track_purchase(cursor, timestamp, amount_usd, country_id, album_id)


def insert_track_sale(cursor: cursor, track_sale: dict) -> None:
    """Inserts data relating to a track (belonging to an album) sale."""

    country = track_sale["country"]
    country_id = get_or_insert_country(cursor, country)

    artist = track_sale["artist_name"]
    artist_url = track_sale["artist_url"]
    artist_id = get_or_insert_artist(cursor, artist, artist_url)

    album_title = track_sale["album_title"]
    album_url = track_sale["album_url"]
    album_id = get_or_insert_album(cursor, album_title, artist_id, album_url)

    for tag in track_sale["album_tags"]:
        get_or_insert_tags(cursor, tag, album_id)

    track_title = track_sale["item_description"]
    track_url = track_sale["url"]
    track_id = get_or_insert_track_or_single(
        cursor, track_title, artist_id, track_url, album_id
    )

    for tag in track_sale["track_tags"]:
        get_or_insert_tags(cursor, tag, -1, track_id)

    timestamp = track_sale["utc_date"]
    amount_usd = track_sale["amount_paid_usd"]
    insert_album_or_track_purchase(
        cursor, timestamp, amount_usd, country_id, -1, track_id
    )


def insert_single_sale(cursor: cursor, single_sale: dict) -> None:
    """Inserts data relating to a single sale."""

    country = single_sale["country"]
    country_id = get_or_insert_country(cursor, country)

    artist = single_sale["artist_name"]
    artist_url = single_sale["artist_url"]
    artist_id = get_or_insert_artist(cursor, artist, artist_url)

    single_title = single_sale["item_description"]
    single_url = single_sale["url"]
    track_id = get_or_insert_track_or_single(
        cursor, single_title, artist_id, single_url
    )

    for tag in single_sale["track_tags"]:
        get_or_insert_tags(cursor, tag, -1, track_id)

    timestamp = single_sale["utc_date"]
    amount_usd = single_sale["amount_paid_usd"]
    insert_album_or_track_purchase(
        cursor, timestamp, amount_usd, country_id, -1, track_id
    )


if __name__ == "__main__":

    load_dotenv()
