"""Script for transforming the data extracted from the api and web-scraping."""

from datetime import datetime, timezone
import logging
from extract import insert_protocol_url, get_stem_url, get_sales_data

KEYS_TO_REMOVE = [
    "slug_type",
    "track_album_slug_text",
    "currency",
    "amount_paid",
    "item_price",
    "art_id",
    "releases",
    "package_image_id",
    "amount_paid_fmt",
    "art_url",
    "amount_over_fmt",
    "item_slug",
    "country_code",
]


def convert_unix_to_datetime(unix_timestamp: float) -> str:
    """Constructs and returns a string representing date and time from a Unix timestamp."""

    if not isinstance(unix_timestamp, float):
        raise TypeError(
            f"Expected a float for unix_timestamp, but got {
                type(unix_timestamp)}"
        )

    if unix_timestamp < 0:
        raise ValueError("Unix timestamp cannot be negative.")

    unix_timestamp_seconds = int(unix_timestamp)

    date_time = datetime.fromtimestamp(unix_timestamp_seconds, tz=timezone.utc)

    utc_date_time_now = datetime.now(timezone.utc)

    if date_time > utc_date_time_now:
        raise ValueError(
            f"The provided Unix timestamp corresponds to a future date or time: {
                date_time}"
        )
    return date_time.strftime("%Y-%m-%d %H:%M:%S")


def clean_data(sales_data: dict) -> dict:
    """Takes the sales data as a dict, and removes specific, unnecessary keys."""

    if not isinstance(sales_data, dict):
        raise TypeError("Input data must be a dictionary.")

    return {
        key: value for key, value in sales_data.items() if key not in KEYS_TO_REMOVE
    }


def clean_tags(tags: list[str]) -> list[str]:
    """Removes leading/trailing whitespace, leading hashtags, and 'lowercases' a list of tags, returning it."""
    if tags is None:
        return []
    return [tag.lstrip("#").strip().lower() for tag in tags]


def transform_sales_data(sales_data: list[dict]) -> list[dict]:
    """Cleans and formats the sales data, returning it as a list of dictionaries."""

    logging.info("Transforming sales data...")

    cleaned_sales = []

    for item in sales_data:

        item["utc_date"] = convert_unix_to_datetime(item["utc_date"])
        item["url"] = insert_protocol_url(item["url"])
        item["artist_url"] = get_stem_url(item["url"])

        item["album_tags"] = clean_tags(item.get("album_tags"))
        item["track_tags"] = clean_tags(item.get("track_tags"))

        cleaned_sales.append(clean_data(item))

    logging.info("Transform complete!")

    return cleaned_sales


if __name__ == "__main__":

    list_of_items = get_sales_data()
    cleaned_data = transform_sales_data(list_of_items)
