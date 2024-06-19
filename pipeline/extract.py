'''File used for extracting information from bandcamp's website and API'''

import logging
import requests as req
from bs4 import BeautifulSoup


'''
Only care if item type t or a
and event type sale
Scrape the tags, album url
if album, give album tags
if track with no album, give track tags (album title == null)
if track with associated album, give album url, album tags, track tags
'''

BANDCAMP_SALES_URL = "https://bandcamp.com/api/salesfeed/1/get_initial"
TEMPLATE_ALBUM_URL = "https://tokenrecords.bandcamp.com/album/"
TEMPLATE_TRACK_URL = "https://tokenrecords.bandcamp.com/track/"
MAX_TIMEOUT_SECONDS = 10


def get_data_from_url(site_url: str = BANDCAMP_SALES_URL, max_timeout: int = MAX_TIMEOUT_SECONDS) -> dict:
    '''Get content from the specified URL'''
    try:
        response = req.get(site_url, timeout=max_timeout)

        if response.status_code == 200:
            response_contents = response.json()

            return response_contents
        else:
            print(f"Failed to retrieve data. HTTP Status code: {
                response.status_code}")

    except req.exceptions.RequestException as e:
        logging.error(f"A request error has occurred: {e}")
    except TimeoutError as e:
        logging.error(f"A timeout error has occurred: {e}")


def extract_list_of_items(event_list: list[dict]) -> list[dict]:
    '''Extract all items from event list, where each element is an item'''
    item_list = []
    for event in event_list:
        if event['event_type'] != 'sale':
            continue
        if len(event['items']) < 1:
            continue

        for item in event['items']:
            if not (item["item_type"] == "a" or item["item_type"] == "t"):
                continue
            item_list.append(extract_and_scrape_item(item))

    return item_list


def extract_and_scrape_item(purchase_dict: dict) -> dict:
    '''Scrape and extract information for an item, giving
    more complete information for the item'''
    if purchase_dict["item_type"] == "t":
        track_url = "https:" + purchase_dict["url"]
        purchase_dict["track_tags"] = scrape_tags(track_url)
    if purchase_dict["item_type"] == "a":
        album_url = TEMPLATE_ALBUM_URL + \
            get_item_type_and_title(purchase_dict["url"])

    return purchase_dict


def get_item_type_and_title(url_string: str) -> str:
    '''Grab the track and album'''
    parts = url_string.split("/")[-2:]
    return "/".join(parts)


def scrape_tags(webpage_url: str) -> list:
    '''Scrapes tags of a specified webpage url'''
    try:
        response = req.get(webpage_url, timeout=MAX_TIMEOUT_SECONDS)
    except req.exceptions.RequestException as e:
        logging.error(f"A request error has occurred: {e}")
        return
    except TimeoutError as e:
        logging.error(f"A timeout error has occurred: {e}")
        return

    tag_list = []

    soup = BeautifulSoup(response.text, features="html.parser")
    stuff = soup.find_all("a", class_="tag")

    for tag in stuff:
        tag_list.append(tag.text)

    return tag_list


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.info("Testing logging")

    data = get_data_from_url()
    if data != None:
        list_of_items = extract_list_of_items(data['feed_data']['events'])
        print(list_of_items[2])

    # print(scrape_tags("https://olson.bandcamp.com/track/cerulean"))
    print(get_item_type_and_title("https://olson.bandcamp.com/track/cerulean"))
