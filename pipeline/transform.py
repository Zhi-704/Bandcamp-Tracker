"""Script for transforming the data extracted from the api and web-scraping."""

from datetime import datetime, timezone


def convert_unix_to_datetime(unix_timestamp: str) -> datetime:
    """Constructs and returns a datetime object from a unix timestamp."""

    try:
        unix = int(float(unix_timestamp))
    except TypeError as e:
        raise TypeError(f"{unix_timestamp} is not a valid unix timestamp!")

    return datetime.fromtimestamp(unix, tz=timezone.utc)


def format_item_url(item_url: str):
    pass


def get_artist_url(item_url: str):
    pass


if __name__ == "__main__":

    print(convert_unix_to_datetime("1718801551.04217"))
