'''File used for extracting information from bandcamp's website and API'''

import json
import logging
import requests as req
from bs4 import BeautifulSoup


BANDCAMP_SALES_URL = "https://bandcamp.com/api/salesfeed/1/get_initial"
MAX_TIMEOUT_SECONDS = 10


def get_data_from_url(site_url: str = BANDCAMP_SALES_URL,
                      max_timeout: int = MAX_TIMEOUT_SECONDS) -> dict:
    '''Get content from the specified URL'''
    try:
        response = req.get(site_url, timeout=max_timeout)

        if response.status_code == 200:
            response_contents = response.json()

            return response_contents
        logging.error("Failed to retrieve data. HTTP Status code: %s",
                      response.status_code)

    except req.exceptions.RequestException as e:
        logging.error("A request error has occurred: %s", e)
    except TimeoutError as e:
        logging.error("A timeout error has occurred: %s", e)
    return None


def extract_list_of_items(event_list: list[dict]) -> list[dict]:
    '''Extract all items from event list, where each element is an item'''
    item_list = []
    counter = 0
    for event in event_list:
        if event['event_type'] != 'sale':
            continue
        if len(event['items']) < 1:
            continue

        for item in event['items']:
            if not (item["item_type"] == "a" or item["item_type"] == "t"):
                continue
            item_list.append(extract_and_scrape_item(item))
            print("Scraped: ", counter)
            counter += 1

    return item_list


def extract_and_scrape_item(purchase_dict: dict) -> dict:
    '''Scrape and extract information for an item, giving
    more complete information for the item'''
    if purchase_dict["item_type"] == "t":
        purchase_dict["track_tags"] = scrape_tags(
            insert_protocol_url(purchase_dict["url"]))
    if purchase_dict["item_type"] == "a":
        purchase_dict["album_tags"] = scrape_tags(
            insert_protocol_url(purchase_dict["url"]))
    if purchase_dict["item_type"] == "t" and purchase_dict["album_title"] is not None:
        stem_url = get_stem_url(insert_protocol_url(purchase_dict["url"]))
        album_url = scrape_album_url(insert_protocol_url(purchase_dict["url"]))

        if stem_url is not None and album_url is not None:
            purchase_dict["album_url"] = stem_url+album_url
            purchase_dict["album_tags"] = scrape_tags(stem_url+album_url)

    return purchase_dict


def save_to_json(list_to_be_written: list) -> None:
    '''Saves list of dictionary to json'''
    with open('sanity_check.json', 'w', encoding='utf-8') as file:
        json.dump(list_to_be_written, file, indent=4)

    logging.info("List of dictionaries has been saved to sanity_check.json")


def insert_protocol_url(url_string: str) -> str:
    '''Checks if protocol is inside url string, if not adds it'''
    if "https://" in url_string or "http://" in url_string:
        return url_string
    return "https:" + url_string


def get_stem_url(url_string: str) -> str:
    '''Grab the stem of a url'''
    parts = url_string.split("/")[:-2]
    return "/".join(parts)


def scrape_album_url(webpage_url: str) -> str:
    '''Scrapes album url of a specified webpage url'''
    try:
        response = req.get(webpage_url, timeout=MAX_TIMEOUT_SECONDS)
    except req.exceptions.RequestException as e:
        logging.error("A request error has occurred scraping album: %s", e)
        return None
    except TimeoutError as e:
        logging.error("A timeout error has occurred scraping album: %s", e)
        return None

    soup = BeautifulSoup(response.text, features="html.parser")
    link = soup.find("a", id="buyAlbumLink")

    if link:
        href = link.get("href")
        if href:
            return href

    return None


def scrape_tags(webpage_url: str) -> list:
    '''Scrapes tags of a specified webpage url'''
    try:
        response = req.get(webpage_url, timeout=MAX_TIMEOUT_SECONDS)
    except req.exceptions.RequestException as e:
        logging.error("A request error has occurred scraping tags: %s", e)
        return
    except TimeoutError as e:
        logging.error("A timeout error has occurred scraping tags: %s", e)
        return

    tag_list = []

    soup = BeautifulSoup(response.text, features="html.parser")
    tags = soup.find_all("a", class_="tag")

    for tag in tags:
        tag_list.append(tag.text)

    return tag_list if len(tag_list) > 0 else None


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.info("Testing logging")

    data = get_data_from_url()
    if data is not None:
        list_of_items = extract_list_of_items(data['feed_data']['events'])
        save_to_json(list_of_items)
