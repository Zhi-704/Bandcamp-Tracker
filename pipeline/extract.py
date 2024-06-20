'''File used for extracting information from bandcamp's website and API'''


import asyncio
import json
import logging
from time import sleep

import aiohttp
from bs4 import BeautifulSoup
import requests as req


BANDCAMP_SALES_URL = "https://bandcamp.com/api/salesfeed/1/get_initial"
MAX_TIMEOUT_SECONDS = 20


def get_sale_data_from_api(site_url: str = BANDCAMP_SALES_URL,
                           max_timeout: int = MAX_TIMEOUT_SECONDS) -> dict:
    '''Get content from the specified api endpoint. Sleep was included to avoid a 429 error'''
    sleep(10)
    try:
        response = req.get(site_url, timeout=max_timeout)

        if response.status_code == 200:
            response_contents = response.json()

            return response_contents
        logging.error("Failed to retrieve sale data from API. HTTP Status code: %s",
                      response.status_code)

    except req.exceptions.RequestException as e:
        logging.error("A request error has occurred: %s", e)
    except TimeoutError as e:
        logging.error("A timeout error has occurred: %s", e)
    return None


def save_to_json(sales_data: list, filename: str) -> None:
    '''Saves list of dictionary to json'''
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(sales_data, file, indent=4)

    logging.info("List of dictionaries has been saved to %s", filename)


def insert_protocol_url(url_string: str) -> str:
    '''Checks if protocol is inside url string, if not adds it'''
    if "https://" in url_string or "http://" in url_string:
        return url_string
    return "https:" + url_string


def get_stem_url(url_string: str) -> str:
    '''Grab the stem of a url'''
    parts = url_string.split("/")[:-2]
    return "/".join(parts)


async def extract_list_of_items(event_list: list[dict],
                                timeout: int = MAX_TIMEOUT_SECONDS) -> list[dict]:
    '''Extract all items from event list, where each element is an item'''
    item_list = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for event in event_list:
            if event['event_type'] != 'sale':
                continue
            if len(event['items']) < 1:
                continue

            for item in event['items']:
                if not (item["item_type"] == "a" or item["item_type"] == "t"):
                    continue
                tasks.append(extract_and_scrape_item(session, item, timeout))

        item_list = await asyncio.gather(*tasks)

    return item_list


async def extract_and_scrape_item(session: aiohttp.ClientSession,
                                  purchase_dict: dict,
                                  timeout: int) -> dict:
    '''Scrape and extract information for an item, giving
    more complete information for the item'''
    if purchase_dict["item_type"] == "t":
        purchase_dict["track_tags"] = await scrape_tags(session,
                                                        insert_protocol_url(
                                                            purchase_dict["url"]),
                                                        timeout)
    if purchase_dict["item_type"] == "a":
        purchase_dict["album_tags"] = await scrape_tags(session,
                                                        insert_protocol_url(
                                                            purchase_dict["url"]),
                                                        timeout)
    if purchase_dict["item_type"] == "t" and purchase_dict["album_title"] is not None:
        stem_url = get_stem_url(insert_protocol_url(purchase_dict["url"]))
        album_url = await scrape_album_url(session,
                                           insert_protocol_url(
                                               purchase_dict["url"]),
                                           timeout)

        if stem_url is not None and album_url is not None:
            purchase_dict["album_url"] = stem_url + album_url
            purchase_dict["album_tags"] = await scrape_tags(session, stem_url + album_url, timeout)

    return purchase_dict


async def fetch_webpage(session: aiohttp.ClientSession, specified_url: str, timeout: int):
    '''Get text/html content from a specified url'''
    try:
        async with session.get(specified_url, timeout=timeout) as response:
            if response.status == 200:
                return await response.text()
            logging.error("Failed to fetch data. HTTP Status code: %s",
                          response.status)
            logging.error("The error specified url is: %s", specified_url)
            return None
    except aiohttp.ClientError as e:
        logging.error("A fetch request error has occurred: %s", e)
    except asyncio.TimeoutError as e:
        logging.error("A fetch timeout error has occurred: %s", e)
    return None


async def scrape_album_url(session: aiohttp.ClientSession, webpage_url: str, timeout: int) -> str:
    '''Scrapes album url of a specified webpage url'''
    html = await fetch_webpage(session, webpage_url, timeout)

    if html is None:
        return None

    soup = BeautifulSoup(html, features="html.parser")
    link = soup.find("a", id="buyAlbumLink")

    if link:
        href = link.get("href")
        if href:
            return href

    return None


async def scrape_tags(session: aiohttp.ClientSession, webpage_url: str, timeout: int) -> list:
    '''Scrapes tags of a specified webpage url'''
    html = await fetch_webpage(session, webpage_url, timeout)
    if html is None:
        return None

    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all("a", class_="tag")
    return [tag.text for tag in tags] if len(tags) > 0 else None


def configure_log() -> None:
    '''Configures log output'''
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def get_sales_data() -> list[dict]:
    '''Get the latest sales data from bandcamp'''

    logging.info("Extraction started")

    sales_data = get_sale_data_from_api()
    logging.info("Sales data gathered")
    if sales_data is not None:
        logging.info("Scraping begun")
        list_of_albums_tracks = asyncio.run(
            extract_list_of_items(sales_data['feed_data']['events']))
        logging.info("Scraping ended")
    else:
        logging.info("Scraping did not initiate")
        return
    logging.info("Extract finished")

    return list_of_albums_tracks


if __name__ == "__main__":
    configure_log()

    logging.info("Extraction started")

    data = get_sale_data_from_api()
    logging.info("Sales data gathered")
    if data is not None:
        logging.info("Scraping begun")
        list_of_items = asyncio.run(
            extract_list_of_items(data['feed_data']['events']))
        save_to_json(list_of_items, "Checking_again.json")
        logging.info("Scraping ended")
    else:
        logging.info("Scraping did not initiate")
    logging.info("Extract finished")
