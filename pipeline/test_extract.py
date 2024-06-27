'''File used to test extract'''

from unittest.mock import patch
import pytest
from extract import insert_protocol_url, get_stem_url, extract_list_of_items


@pytest.mark.parametrize("url_string, expected", [
    ("https://example.com", "https://example.com"),
    ("http://example.com", "http://example.com"),
    ("//example.com", "https://example.com"),
    ("", "https:"),
    ("https://example.com/path", "https://example.com/path"),
    ("//example.com/path", "https://example.com/path")
])
def test_insert_protocol_url(url_string, expected):
    '''Test insert protocol function with expected output'''
    assert insert_protocol_url(url_string) == expected


@pytest.mark.parametrize("url_string, expected", [
    ("https://example.com/path/to/resource", "https://example.com/path"),
    ("http://example.com/a/b/c/d", "http://example.com/a/b"),
    ("https://example.com/one/two", "https://example.com"),
    ("http://example.com/justonelevel", "http:/"),
    ("https://example.com", "https:"),
    ("//example.com/path/to/resource", "//example.com/path"),
    ("example.com/a/b/c", "example.com/a")
])
def test_get_stem_url(url_string, expected):
    '''Tests if stem url being correctly retrieved'''
    assert get_stem_url(url_string) == expected


class TestExtractItems():
    '''Class for extracting items'''

    event_list = [
        {"event_type": "sale", "items": [
            {"item_type": "a", "url": "https://example.com/a"}]},
        {"event_type": "sale", "items": [
            {"item_type": "t", "url": "https://example.com/t"}]},
    ]

    expected_items = [
        {"item_type": "a", "url": "https://example.com/a",
            "tags": ["tag1", "tag2"]},
        {"item_type": "t", "url": "https://example.com/t",
            "tags": ["tag3", "tag4"]},
    ]

    # pylint: disable=unused-argument
    async def mock_extract_and_scrape_item(self, sempahore, session, item, timeout):
        '''Fake function to use'''
        if item["url"] == "https://example.com/a":
            return {"item_type": "a", "url": item["url"], "tags": ["tag1", "tag2"]}
        if item["url"] == "https://example.com/t":
            return {"item_type": "t", "url": item["url"], "tags": ["tag3", "tag4"]}

    @pytest.mark.asyncio
    async def test_extract_list_of_items_base_case(self):
        '''Tests for normal case'''
        with patch('extract.extract_and_scrape_item', new=self.mock_extract_and_scrape_item):
            items = await extract_list_of_items(self.event_list)
            assert items == self.expected_items

    @pytest.mark.asyncio
    async def test_extract_list_of_items_no_sales(self):
        '''Tests for when there are no sales item'''
        no_sales_data = [{"event_type": "not_a_sale", "items": [
            {"item_type": "a", "url": "https://example.com/a"}]}]
        with patch('extract.extract_and_scrape_item', new=self.mock_extract_and_scrape_item):
            items = await extract_list_of_items(no_sales_data)
            assert items == []

    @pytest.mark.asyncio
    async def test_extract_list_of_items_empty_input(self):
        '''Test for empty input'''
        items = await extract_list_of_items([])
        assert items == []
