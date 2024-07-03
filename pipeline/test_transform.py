"""Tests for transform functions."""

import pytest
from transform import convert_unix_to_datetime, clean_data, transform_sales_data, clean_tags


@pytest.mark.parametrize(
    "unix_float, expected_output",
    [
        (1718801551.04217, "2024-06-19 12:52:31"),
        (1718715151.04217, "2024-06-18 12:52:31"),
        (1718628751.04217, "2024-06-17 12:52:31"),
        (1718542351.04217, "2024-06-16 12:52:31"),
        (1718455951.04217, "2024-06-15 12:52:31"),
    ],
)
def test_convert_unix_to_datetime_valid(unix_float, expected_output):
    """Tests that a valid Unix timestamp is converted to a string."""
    assert convert_unix_to_datetime(unix_float) == expected_output


@pytest.mark.parametrize(
    "unix_timestamp, expected_exception, expected_message",
    [
        (
            "171880151.04217",
            TypeError,
            "Expected a float for unix_timestamp, but got <class 'str'>",
        ),
        (-1718801551.04217, ValueError, "Unix timestamp cannot be negative."),
        (
            9918801551.04217,
            ValueError,
            "The provided Unix timestamp corresponds to a future date or time: ",
        ),
    ],
)
def test_convert_unix_to_datetime_exceptions(
    unix_timestamp, expected_exception, expected_message
):
    """Tests that the appropriate exceptions are raised for invalid inputs."""
    with pytest.raises(expected_exception) as exc_info:
        convert_unix_to_datetime(unix_timestamp)
    assert str(exc_info.value).startswith(expected_message)


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
                "Belfast"]
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
                "belfast",
            ],
            "track_tags": [],
            "artist_url": "https://example_artist.bandcamp.com",
        }
    ]

    assert transform_sales_data(input_data) == expected_output


def test_clean_tags_normal_case():
    """Tests that tags are properly cleaned in normal cases."""
    tags = [" TagOne ", "##TAGTWO", "#tagthree "]
    expected = ["tagone", "tagtwo", "tagthree"]
    assert clean_tags(tags) == expected


def test_clean_tags_empty_list():
    """Tests that an empty list is handled correctly."""
    tags = []
    expected = []
    assert clean_tags(tags) == expected


def test_clean_tags_none():
    """Tests that 'None' is handled correctly."""
    tags = None
    expected = []
    assert clean_tags(tags) == expected


def test_clean_tags_whitespace_only():
    """Tests that only whitespace is handled correctly."""
    tags = [" ", "   ", " \t "]
    expected = ["", "", ""]
    assert clean_tags(tags) == expected
