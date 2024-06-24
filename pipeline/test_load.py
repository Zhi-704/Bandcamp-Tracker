"""Tests for the load script."""

import os
from unittest.mock import patch, MagicMock, call
import psycopg2
from load import (
    get_connection,
    get_cursor,
    get_or_insert_artist,
    get_or_insert_country,
    get_or_insert_album,
    get_or_insert_track_or_single,
    get_or_insert_tags,
    insert_album_or_track_purchase,
    insert_album_sale,
    insert_track_sale,
    insert_single_sale,
)


@patch.dict(
    os.environ,
    {
        "DB_HOST": "localhost",
        "DB_NAME": "test_db",
        "DB_USER": "test_user",
        "DB_PASS": "test_pass",
        "DB_PORT": "test_port",
    },
)
@patch("load.psycopg2.connect")
def test_get_connection(mock_connect):
    """Test case for get_connection function."""
    mock_connect.return_value = "mock_connection"
    connection = get_connection()
    assert connection == "mock_connection"
    mock_connect.assert_called_once()


@patch("load.get_connection")
def test_get_cursor(mock_get_connection):
    """Test case for get_cursor function."""
    mock_connection = MagicMock()
    mock_get_connection.return_value = mock_connection
    cursor = get_cursor(mock_connection)
    mock_connection.cursor.assert_called_once_with(
        cursor_factory=psycopg2.extras.DictCursor
    )
    assert cursor == mock_connection.cursor()


@patch("load.get_cursor")
def test_get_or_insert_artist_existing(mock_get_cursor):
    """Test case for get_or_insert_artist with existing artist."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    artist_id = get_or_insert_artist(mock_cursor, "artist_name", "artist_url")
    assert artist_id == 1
    mock_cursor.execute.assert_called_with(
        "SELECT artist_id FROM artist WHERE artist.name = %s AND artist.url = %s",
        ("artist_name", "artist_url"),
    )


@patch("load.get_cursor")
def test_get_or_insert_artist_new(mock_get_cursor):
    """Test case for get_or_insert_artist with new artist."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [None, [2]]
    artist_id = get_or_insert_artist(
        mock_cursor, "new_artist_name", "new_artist_url")
    assert artist_id == 2
    mock_cursor.execute.assert_called_with(
        "INSERT INTO artist(name, url) VALUES (%s, %s) RETURNING artist_id",
        ("new_artist_name", "new_artist_url"),
    )


@patch("load.get_cursor")
def test_get_or_insert_country_existing(mock_get_cursor):
    """Test case for get_or_insert_country with existing country."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    country_id = get_or_insert_country(mock_cursor, "country_name")
    assert country_id == 1
    mock_cursor.execute.assert_called_with(
        "SELECT country_id FROM country WHERE country.name = %s", (
            "country_name",)
    )


@patch("load.get_cursor")
def test_get_or_insert_country_new(mock_get_cursor):
    """Test case for get_or_insert_country with new country."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [None, [3]]
    country_id = get_or_insert_country(mock_cursor, "new_country_name")
    assert country_id == 3
    mock_cursor.execute.assert_called_with(
        "INSERT INTO country(name) VALUES (%s) RETURNING country_id",
        ("new_country_name",),
    )


@patch("load.get_cursor")
def test_get_or_insert_album_existing(mock_get_cursor):
    """Test case for get_or_insert_album with existing album."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    album_id = get_or_insert_album(mock_cursor, "album_title", 1, "album_url")
    assert album_id == 1
    mock_cursor.execute.assert_called_with(
        "SELECT album_id FROM album WHERE album.title = %s\
            AND album.artist_id = %s AND album.url = %s",
        ("album_title", 1, "album_url"),
    )


@patch("load.get_cursor")
def test_get_or_insert_album_new(mock_get_cursor):
    """Test case for get_or_insert_album with new album."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [None, [2]]
    album_id = get_or_insert_album(
        mock_cursor, "new_album_title", 1, "new_album_url")
    assert album_id == 2
    mock_cursor.execute.assert_called_with(
        "INSERT INTO album(title, artist_id, url) VALUES (%s, %s, %s) RETURNING album_id",
        ("new_album_title", 1, "new_album_url"),
    )


@patch("load.get_cursor")
def test_get_or_insert_track_or_single_existing(mock_get_cursor):
    """Test case for get_or_insert_track_or_single with existing track/single."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    track_id = get_or_insert_track_or_single(
        mock_cursor, "song_title", 1, "song_url")
    assert track_id == 1
    mock_cursor.execute.assert_called_with(
        "SELECT track_id FROM track WHERE track.title = %s\
            AND track.artist_id = %s AND track.url = %s",
        ("song_title", 1, "song_url"),
    )


@patch("load.get_cursor")
def test_get_or_insert_track_or_single_new(mock_get_cursor):
    """Test case for get_or_insert_track_or_single with new track/single."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [None, [2]]
    track_id = get_or_insert_track_or_single(
        mock_cursor, "new_song_title", 1, "new_song_url"
    )
    assert track_id == 2
    mock_cursor.execute.assert_called_with(
        "INSERT INTO track(title, artist_id, url) VALUES (%s, %s, %s) RETURNING track_id",
        ("new_song_title", 1, "new_song_url"),
    )


@patch("load.get_cursor")
def test_get_or_insert_tags_new(mock_get_cursor):
    """Test case for get_or_insert_tags with new tag."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [None, [1]]
    get_or_insert_tags(mock_cursor, "new_tag", album_id=1)
    calls = [
        call("SELECT tag_id FROM tag WHERE name = %s", ("new_tag",)),
        call("INSERT INTO tag(name) VALUES (%s) RETURNING tag_id", ("new_tag",)),
        call(
            "INSERT INTO album_tag_assignment(tag_id, album_id) VALUES (%s, %s)", (
                1, 1)
        ),
    ]
    mock_cursor.execute.assert_has_calls(calls)


@patch("load.get_cursor")
def test_get_or_insert_tags_existing(mock_get_cursor):
    """Test case for get_or_insert_tags with existing tag."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    get_or_insert_tags(mock_cursor, "existing_tag", album_id=1)
    calls = [
        call("SELECT tag_id FROM tag WHERE name = %s", ("existing_tag",)),
        call(
            "INSERT INTO album_tag_assignment(tag_id, album_id) VALUES (%s, %s)", (
                1, 1)
        ),
    ]
    mock_cursor.execute.assert_has_calls(calls)


@patch("load.get_cursor")
def test_insert_album_or_track_purchase_album(mock_get_cursor):
    """Test case for insert_album_or_track_purchase with album purchase."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor
    insert_album_or_track_purchase(
        mock_cursor, "timestamp", 10.0, 1, album_id=1)
    mock_cursor.execute.assert_called_with(
        "INSERT INTO album_purchase(album_id, timestamp, amount_usd, country_id)\
                VALUES (%s, %s, %s, %s)",
        (1, "timestamp", 10.0, 1),
    )


@patch("load.get_cursor")
def test_insert_album_or_track_purchase_track(mock_get_cursor):
    """Test case for insert_album_or_track_purchase with track purchase."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor
    insert_album_or_track_purchase(
        mock_cursor, "timestamp", 10.0, 1, track_id=1)
    mock_cursor.execute.assert_called_with(
        "INSERT INTO track_purchase(track_id, timestamp, amount_usd, country_id)\
                VALUES (%s, %s, %s, %s)",
        (1, "timestamp", 10.0, 1),
    )


@patch("load.get_cursor")
def test_insert_album_sale(mock_get_cursor):
    """Test case for insert_album_sale function."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor
    album_sale = {
        "utc_date": 1718881844.178138,
        "artist_name": "FINAL",
        "item_type": "a",
        "item_description": "Infinite Guitar 2",
        "currency": "USD",
        "amount_paid": 2.0,
        "item_price": 0.0,
        "amount_paid_usd": 2.0,
        "country": "United Kingdom",
        "art_id": 3978634151,
        "url": "https://final1.bandcamp.com/album/infinite-guitar-2",
        "artist_url": "https://final1.bandcamp.com",
        "country_code": "gb",
        "amount_paid_fmt": "$2",
        "art_url": "https://f4.bcbits.com/img/a3978634151_7.jpg",
        "album_tags": [
            "ambient",
            "experimental",
            "industrial",
            "noise",
            "power electronics",
            "United Kingdom",
        ],
    }
    insert_album_sale(mock_cursor, album_sale)

    assert mock_cursor.fetchone.call_count == 9
    assert mock_cursor.execute.call_count == 16


@patch("load.get_cursor")
def test_insert_track_sale(mock_get_cursor):
    """Test case for insert_track_sale function."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor

    track_sale = {
        "utc_date": 1718881757.3350313,
        "artist_name": "Symptoms of Love",
        "item_type": "t",
        "item_description": "Foam (Streetside Mix)",
        "album_title": "PT002 - Foam EP",
        "amount_paid_usd": 2.0,
        "country": "France",
        "url": "//planettriprecords.bandcamp.com/track/foam-streetside-mix",
        "track_tags": ["electronic", "street soul", "downtempo", "Sydney"],
        "album_url": "https://planettriprecords.bandcamp.com/album/pt002-foam-ep",
        "artist_url": "https://planettriprecords.bandcamp.com",
    }

    insert_track_sale(mock_cursor, track_sale)

    assert mock_cursor.fetchone.call_count == 8
    assert mock_cursor.execute.call_count == 13


@patch("load.get_cursor")
def test_insert_single_sale(mock_get_cursor):
    """Test case for insert_single_sale function."""
    mock_cursor = MagicMock()
    mock_get_cursor.return_value = mock_cursor

    single_sale = {
        "utc_date": 1718881780.3168454,
        "artist_name": "Jealous of the Birds",
        "item_type": "t",
        "item_description": "Mrs Dalloway",
        "album_title": None,
        "currency": "GBP",
        "amount_paid": 2.0,
        "item_price": 0.0,
        "amount_paid_usd": 2.54,
        "country": "United Kingdom",
        "url": "//jealousofthebirds.bandcamp.com/track/mrs-dalloway",
        "artist_url": "https://jealousofthebirds.bandcamp.com",
        "track_tags": [
            "alternative",
            "acoustic punk",
            "indie",
            "indie folk",
            "singer-songwriter",
            "Belfast",
        ],
    }

    insert_single_sale(mock_cursor, single_sale)

    assert mock_cursor.fetchone.call_count == 9
    assert mock_cursor.execute.call_count == 16
