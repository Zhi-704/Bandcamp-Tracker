"""Tests for transform functions."""

from transform import convert_unix_to_datetime, format_item_url, get_artist_url
from datetime import datetime, timezone


def test_convert_unix_to_datetime_valid():

    unix_timestamp = "1718801551.04217"

    assert convert_unix_to_datetime(
        unix_timestamp) == datetime(2024, 6, 19, 12, 52, 31, tzinfo=timezone.utc)


def test_convert_unix_to_datetime_valid():

    unix_timestamp = "1718801551.04217"

    assert convert_unix_to_datetime(
        unix_timestamp) == datetime(2024, 6, 19, 12, 52, 31, tzinfo=timezone.utc)
