"""Tests for the pipeline script."""

from datetime import datetime
import pytest
from unittest.mock import patch
from pipeline import main


@pytest.fixture
def mock_sales_data():
    return [
        {
            "utc_date": datetime(2024, 6, 30),
            "url": "https://example.com/album",
            "artist_name": "Artist Name",
            "artist_url": "https://example.com/artist",
            "item_type": "a",
            "item_description": "Album Title",
            "album_tags": ["tag1", "tag2"],
            "amount_paid_usd": 10.0,
            "country": "Country A"
        },
        {
            "utc_date": datetime(2024, 6, 29),
            "url": "https://example.com/track",
            "artist_name": "Artist Name",
            "artist_url": "https://example.com/artist",
            "item_type": "t",
            "item_description": "Track Title",
            "album_title": "Album Title",
            "album_url": "https://example.com/album",
            "track_tags": ["tag3", "tag4"],
            "amount_paid_usd": 5.0,
            "country": "Country B"
        }
    ]


@patch('pipeline.get_sales_data')
@patch('pipeline.transform_sales_data')
@patch('pipeline.load_sales_data')
def test_etl_pipeline(mock_load_sales_data, mock_transform_sales_data, mock_get_sales_data, mock_sales_data):
    """Tests that the E,T, and L functions are all called once."""
    mock_get_sales_data.return_value = mock_sales_data
    mock_transform_sales_data.return_value = mock_sales_data

    main('foo', 'bar')

    mock_get_sales_data.assert_called_once()
    mock_transform_sales_data.assert_called_once_with(mock_sales_data)
    mock_load_sales_data.assert_called_once_with(mock_sales_data)
