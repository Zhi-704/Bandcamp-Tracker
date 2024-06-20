"""Tests for transform functions."""

from transform import convert_unix_to_datetime, clean_data, transform_sales_data
import pytest


def test_convert_unix_to_datetime_valid():
    """Tests that a valid Unix timestamp is converted to a string.."""

    unix_timestamp = 1718801551.04217

    assert convert_unix_to_datetime(unix_timestamp) == "2024-06-19 12:52:31"


def test_convert_unix_to_datetime_invalid_type():
    """Tests that a TypeError is raised if a float is not passed in."""

    unix_timestamp = "171880151.04217"

    with pytest.raises(TypeError) as exc_info:
        convert_unix_to_datetime(unix_timestamp)
        assert (
            str(exc_info.value)
            == "Expected a float for unix_timestamp, but got <class 'str'>"
        )


def test_convert_unix_to_datetime_invalid_unix():
    """Tests that a ValueError is raised when a invalid Unix is passed in."""

    unix_timestamp = -1718801551.04217

    with pytest.raises(ValueError) as exc_info:
        convert_unix_to_datetime(unix_timestamp)
    assert str(exc_info.value) == "Unix timestamp cannot be negative."


def test_convert_unix_to_datetime_invalid_datetime():
    """Tests that a ValueError is raised if an 'impossible' unix is passed in."""

    unix_timestamp = 9918801551.04217

    with pytest.raises(ValueError) as exc_info:
        convert_unix_to_datetime(unix_timestamp)
    assert str(exc_info.value).startswith(
        "The provided Unix timestamp corresponds to a future date or time: "
    )


def test_clean_data_valid():
    """Tests that the correct keys are removed from the dictionary."""

    input_data = {
        "slug_type": "track",
        "track_album_slug_text": "some_slug",
        "artist": "Artist Name",
        "track_title": "Song Title",
        "currency": "USD",
        "amount_paid": 1.99,
        "country_code": "US",
        "item_price": 1.29,
        "art_id": 12345,
        "releases": [{"id": 67890}],
        "package_image_id": 98765,
        "amount_paid_fmt": "$1.99",
        "art_url": "https://example.com/image.jpg",
        "amount_over_fmt": "$0.70",
        "item_slug": "song-title",
    }

    expected_output = {
        "artist": "Artist Name",
        "track_title": "Song Title",
    }

    assert clean_data(input_data) == expected_output


def test_clean_data_empty_input():
    """Test that it performs as expected with an empty dictionary."""
    input_data = {}
    expected_output = {}

    assert clean_data(input_data) == expected_output


def test_clean_data_invalid():
    """Test with invalid input type (not a dictionary)."""

    input_data = "foobar"
    with pytest.raises(TypeError):
        clean_data(input_data)


def test_transform_sales_data_valid():
    """Tests that the expected, cleaned dictionary is returned."""

    input_data = [
        {
            "utc_date": 1718891188.2938294,
            "artist_name": "example_artist",
            "item_type": "a",
            "item_description": "Fine Art",
            "album_title": None,
            "slug_type": "a",
            "track_album_slug_text": None,
            "currency": "GBP",
            "amount_paid": 4.99,
            "item_price": 4.989999771118164,
            "amount_paid_usd": 6.33,
            "country": "Canada",
            "art_id": 2365536250,
            "releases": None,
            "package_image_id": None,
            "url": "//example_artist.bandcamp.com/album/fine-art",
            "country_code": "ca",
            "amount_paid_fmt": "£4.99",
            "art_url": "https://example_artistcom/img/image.jpg",
            "album_tags": [
                "hip hop",
                "hip-hop/rap",
                "irish rap",
                "punk",
                "rap",
                "Belfast",
            ],
        }
    ]

    expected_output = [
        {
            "utc_date": "2024-06-20 13:46:28",
            "artist_name": "example_artist",
            "item_type": "a",
            "item_description": "Fine Art",
            "album_title": None,
            "amount_paid_usd": 6.33,
            "country": "Canada",
            "url": "https://example_artist.bandcamp.com/album/fine-art",
            "album_tags": [
                "hip hop",
                "hip-hop/rap",
                "irish rap",
                "punk",
                "rap",
                "Belfast",
            ],
            "artist_url": "https://example_artist.bandcamp.com",
        }
    ]

    assert transform_sales_data(input_data) == expected_output
