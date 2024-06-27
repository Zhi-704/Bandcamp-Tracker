"""Script containing functions for loading sales data into the Database."""

from os import environ as ENV
import logging
from typing import Any, Dict, List, Optional
import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection as DBConnection, cursor as DBCursor
from dotenv import load_dotenv

from extract import get_sales_data
from transform import transform_sales_data

REQUIRED_FIELDS_TRACK = ["album_url", "track_tags"]
REQUIRED_FIELDS_SINGLE = ["track_tags"]
REQUIRED_FIELDS_ALBUM = ["album_tags"]


def get_connection() -> DBConnection:
    """Creates a database session and returns a connection object."""
    return psycopg2.connect(
        host=ENV["DB_HOST"],
        port=ENV["DB_PORT"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASS"],
        database=ENV["DB_NAME"],
    )


def get_cursor(connection: DBConnection) -> DBCursor:
    """Creates and returns a cursor to execute PostgreSQL commands."""
    return connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def get_or_insert_artist(cursor: DBCursor, artist_name: str, artist_url: str) -> int:
    """Adds the artist to the artist table and returns the artist_id if not present,
    otherwise gets the artist_id from the table"""

    cursor.execute(
        "SELECT artist_id FROM artist WHERE artist.name = %s AND artist.url = %s",
        (
            artist_name,
            artist_url,
        ),
    )
    artist_id = cursor.fetchone()

    if artist_id:
        return artist_id[0]

    cursor.execute(
        "INSERT INTO artist(name, url) VALUES (%s, %s) RETURNING artist_id",
        (artist_name, artist_url),
    )
    return cursor.fetchone()[0]


def get_or_insert_country(cursor: DBCursor, country_name: str) -> int:
    """Adds the country to the country table and returns the country_id if not present,
    otherwise gets the country_id from the table."""

    cursor.execute(
        "SELECT country_id FROM country WHERE country.name = %s", (country_name,)
    )
    country_id = cursor.fetchone()

    if country_id:
        return country_id[0]

    cursor.execute(
        "INSERT INTO country(name) VALUES (%s) RETURNING country_id", (country_name,)
    )
    return cursor.fetchone()[0]


def get_or_insert_album(
    cursor: DBCursor, album_title: str, artist_id: int, album_url: str
) -> int:
    """Adds the album to the album table and returns the album_id if not present,
    otherwise gets the album_id from the table."""

    cursor.execute(
        "SELECT album_id FROM album WHERE album.title = %s AND album.url = %s",
        (album_title, album_url),
    )
    album_id = cursor.fetchone()

    if album_id:
        return album_id[0]

    cursor.execute(
        "INSERT INTO album(title, artist_id, url) VALUES (%s, %s, %s) RETURNING album_id",
        (album_title, artist_id, album_url),
    )
    return cursor.fetchone()[0]


def get_or_insert_track_or_single(
    cursor: DBCursor,
    song_title: str,
    artist_id: int,
    song_url: str,
    album_id: Optional[int] = None,
) -> int:
    """Adds a track or single to the track table, returning the id, if not present,
    otherwise gets the track_id from the table."""

    cursor.execute(
        "SELECT track_id FROM track WHERE track.title = %s\
            AND track.artist_id = %s AND track.url = %s",
        (song_title, artist_id, song_url),
    )
    track_id = cursor.fetchone()

    if track_id:
        return track_id[0]

    if album_id is not None:
        cursor.execute(
            "INSERT INTO track(title, album_id, artist_id, url)\
                VALUES (%s, %s, %s, %s) RETURNING track_id",
            (song_title, album_id, artist_id, song_url),
        )
    else:
        cursor.execute(
            "INSERT INTO track(title, artist_id, url) VALUES (%s, %s, %s) RETURNING track_id",
            (song_title, artist_id, song_url),
        )
    return cursor.fetchone()[0]


def get_or_insert_tags_and_assignments(
    cursor: DBCursor,
    tag_name: str,
    album_id: Optional[int] = None,
    track_id: Optional[int] = None,
) -> None:
    """
    Adds a tag to the tag table and returns the tag_id if it doesn't already exist,
    otherwise simply returns tag_id from table.
    Then checks if the album-tag or track-tag assignment exists in the database,
    inserts it otherwise.
    """

    cursor.execute("SELECT tag_id FROM tag WHERE name = %s", (tag_name,))
    tag_id = cursor.fetchone()
    if not tag_id:
        cursor.execute(
            "INSERT INTO tag(name) VALUES (%s) RETURNING tag_id", (tag_name,)
        )
        tag_id = cursor.fetchone()[0]
    else:
        tag_id = tag_id[0]

    if album_id:

        cursor.execute(
            "SELECT album_tag_assignment_id from album_tag_assignment WHERE album_id = %s and tag_id = %s",
            (album_id, tag_id),
        )
        ata_id = cursor.fetchone()
        if not ata_id:
            cursor.execute(
                "INSERT INTO album_tag_assignment(tag_id, album_id) VALUES (%s, %s)",
                (tag_id, album_id),
            )
    if track_id:
        cursor.execute(
            "SELECT track_tag_assignment_id from album_tag_assignment WHERE track_id = %s and tag_id = %s",
            (track_id, tag_id),
        )
        tta_id = cursor.fetchone()
        if not tta_id:
            cursor.execute(
                "INSERT INTO track_tag_assignment(tag_id, track_id) VALUES (%s, %s)",
                (tag_id, track_id),
            )


def insert_album_or_track_purchase(
    cursor: DBCursor,
    timestamp: str,
    amount_usd: float,
    country_id: int,
    album_id: Optional[int] = None,
    track_id: Optional[int] = None,
) -> None:
    """Inserts an album or track purchase in the (album/track)_purchase table."""

    if album_id:
        cursor.execute(
            "INSERT INTO album_purchase(album_id, timestamp, amount_usd, country_id)\
                VALUES (%s, %s, %s, %s)",
            (album_id, timestamp, amount_usd, country_id),
        )
    elif track_id:
        cursor.execute(
            "INSERT INTO track_purchase(track_id, timestamp, amount_usd, country_id)\
                VALUES (%s, %s, %s, %s)",
            (track_id, timestamp, amount_usd, country_id),
        )


def insert_album_sale(cursor: DBCursor, album_sale: Dict[str, Any]) -> None:
    """Inserts data relating to an album sale."""

    if not all(
        field in album_sale and album_sale[field] for field in REQUIRED_FIELDS_ALBUM
    ):
        logging.warning(
            "Skipping album sale due to missing required fields: %s", album_sale
        )
        return

    country_id = get_or_insert_country(cursor, album_sale["country"])
    artist_id = get_or_insert_artist(
        cursor, album_sale["artist_name"], album_sale["artist_url"]
    )
    album_id = get_or_insert_album(
        cursor, album_sale["item_description"], artist_id, album_sale["url"]
    )
    for tag in album_sale["album_tags"]:
        if tag:
            get_or_insert_tags_and_assignments(cursor, tag, album_id)

    insert_album_or_track_purchase(
        cursor,
        album_sale["utc_date"],
        album_sale["amount_paid_usd"],
        country_id,
        album_id=album_id,
    )


def insert_track_sale(cursor: DBCursor, track_sale: Dict[str, Any]) -> None:
    """Inserts data relating to a track (belonging to an album) sale."""

    if not all(
        field in track_sale and track_sale[field] for field in REQUIRED_FIELDS_TRACK
    ):
        logging.warning(
            "Skipping track sale due to missing required fields: %s", track_sale
        )
        return

    country_id = get_or_insert_country(cursor, track_sale["country"])
    artist_id = get_or_insert_artist(
        cursor, track_sale["artist_name"], track_sale["artist_url"]
    )
    album_id = get_or_insert_album(
        cursor, track_sale["album_title"], artist_id, track_sale["album_url"]
    )

    track_id = get_or_insert_track_or_single(
        cursor, track_sale["item_description"], artist_id, track_sale["url"], album_id
    )

    for tag in track_sale["track_tags"]:
        if tag:
            get_or_insert_tags_and_assignments(cursor, tag, track_id=track_id)

    insert_album_or_track_purchase(
        cursor,
        track_sale["utc_date"],
        track_sale["amount_paid_usd"],
        country_id,
        track_id=track_id,
    )


def insert_single_sale(cursor: DBCursor, single_sale: Dict[str, Any]) -> None:
    """Inserts data relating to a single sale."""

    if not all(
        field in single_sale and single_sale[field] for field in REQUIRED_FIELDS_SINGLE
    ):
        logging.warning(
            "Skipping single sale due to missing required fields: %s, single_sale"
        )
        return

    country_id = get_or_insert_country(cursor, single_sale["country"])
    artist_id = get_or_insert_artist(
        cursor, single_sale["artist_name"], single_sale["artist_url"]
    )
    track_id = get_or_insert_track_or_single(
        cursor, single_sale["item_description"], artist_id, single_sale["url"]
    )

    for tag in single_sale["track_tags"]:
        if tag:
            get_or_insert_tags_and_assignments(cursor, tag, track_id=track_id)

    insert_album_or_track_purchase(
        cursor,
        single_sale["utc_date"],
        single_sale["amount_paid_usd"],
        country_id,
        track_id=track_id,
    )


def load_sales_data(sales_data: List[Dict[str, Any]]) -> None:
    """Loads sales data into the database."""

    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            for sale in sales_data:
                logging.info("Processing sale: %s", sale)
                if sale["item_type"] == "a":
                    logging.info("Inserting album sale")
                    insert_album_sale(cursor, sale)
                elif sale["item_type"] == "t":
                    if sale.get("album_title"):
                        logging.info("Inserting track sale")
                        insert_track_sale(cursor, sale)
                else:
                    logging.info("Inserting single sale")
                    insert_single_sale(cursor, sale)
        connection.commit()
    except Exception as e:
        logging.error("An error occurred: %s", e)
    finally:
        connection.close()


if __name__ == "__main__":

    load_dotenv()

    list_of_items = get_sales_data()
    cleaned_data = transform_sales_data(list_of_items)
    load_sales_data(cleaned_data)
