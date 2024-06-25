from os import environ as ENV
from dotenv import load_dotenv
import logging

from psycopg import connect, Connection
from psycopg.rows import dict_row
from boto3 import client


TRENDING_THRESHOLD = 100
FILTER_TOPICS_BY = "c11-bandcamp-"
TRENDING_TIMEFRAME = '8 hours'


def get_connection() -> Connection:
    """gets a connection"""
    return connect(
        port=ENV["DB_PORT"],
        dbname=ENV["DB_NAME"],
        host=ENV["DB_ENDPOINT"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"],
        row_factory=dict_row
    )


def get_sns_client() -> client:
    '''Creates sns client'''
    return client('sns',
                  aws_access_key_id=ENV["ACCESS_KEY"],
                  aws_secret_access_key=ENV["SECRET_ACCESS_KEY"]
                  )


def filter_topics(filter_word: str, topic_list: list[dict]) -> list[dict]:
    '''Filters list of topics with relevant topics that have a specific word'''
    return [topic for topic in topic_list if filter_word in topic['TopicArn']]


def get_topics_arns_from_aws(sns_client: client) -> list[dict]:
    '''Gets all available topics on AWS'''
    response = sns_client.list_topics()
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Topics']
    return None


def get_tag_arn(tag: str, arn_list: list[dict]) -> list[str]:
    '''Get the arn of a specific tag if it exists'''
    return [arn['TopicArn'] for arn in arn_list if tag in arn['TopicArn']]


def get_sales_data_of_tag(conn: Connection, item_type: str, tag: str, sales_limit: int = TRENDING_THRESHOLD, sales_timeframe: str = TRENDING_TIMEFRAME) -> list[dict]:
    '''Gets trending sales data'''

    query = f'''
SELECT
    T.{item_type}_id,
    T.title,
    A.name AS band,
    COUNT(DISTINCT TP.{item_type}_purchase_id) AS copies_sold,
    T.url
FROM {item_type}_purchase AS TP
JOIN {item_type} AS T ON TP.{item_type}_id = T.{item_type}_id
JOIN artist AS A ON T.artist_id = A.artist_id
JOIN {item_type}_tag_assignment AS TTA ON T.{item_type}_id = TTA.{item_type}_id
JOIN tag AS TG ON TTA.tag_id = TG.tag_id
WHERE TG.name = %s
AND TP.timestamp >= NOW() - INTERVAL '{sales_timeframe}'
GROUP BY
    T.{item_type}_id,
    T.title,
    A.name,
    T.url
HAVING COUNT(DISTINCT TP.{item_type}_purchase_id) >= %s
ORDER BY copies_sold DESC
'''

    try:
        with conn.cursor() as cur:
            cur.execute(query, (tag, sales_limit))
            trending = cur.fetchall()

        if len(trending) >= 1:
            return trending
    except Exception as e:
        logging.error(
            "Error fetching sales data for %s and tag %s: %s", item_type, tag, e)
        conn.rollback()

    return []


def extract_tag_name(topic_arn: str) -> str:
    '''Extracts the tag name from the topic arn'''
    raw_tag = topic_arn.split(':')[-1]
    tag_parts = raw_tag.split('-')[2:]
    return ' '.join(tag_parts)


def configure_log() -> None:
    '''Configures log output'''
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def publish_list_to_topic(sns_client: client, topic_arn: str,  tag: str, trending_data: list[dict]) -> dict:
    '''Publishes trending items for a tag to a topic, which sends an email to all subscribers'''

    subject = f"What's trending for {tag}?"
    message = f"These items are trending for the tag {tag}!\n\n"
    for item in trending_data:
        item_name = item['title']
        item_author = item['band']
        item_type = item['type'].title()
        item_url = item['url']

        message += f"{item_type} '{item_name}' by '{
            item_author}' is currently trending!\n"
        message += f"Check it out here at: {item_url}\n\n"

    response = sns_client.publish(
        TopicArn=topic_arn,
        Subject=subject,
        Message=message,
    )
    return response


def add_tags_to_dictionary(tags_list: list[dict]) -> list[dict]:
    '''Grabs the tags from list of arns'''
    for tag_arn in tags_list:
        topic_arn = tag_arn['TopicArn']
        tag_name = extract_tag_name(topic_arn)
        tag_arn['Tag'] = tag_name
    return tags_list


def get_trending_items(conn: Connection, item_type: str, tag_name: str) -> list[dict]:
    '''Grabs trending data for a specific item type and adds its type to the dictionary'''
    trending_items = get_sales_data_of_tag(
        conn, item_type, tag_name)

    logging.info("Trending %s (%s) : %s", item_type,
                 tag_name, trending_items)

    for item in trending_items:
        item['type'] = item_type

    return trending_items


def notification_system() -> None:
    conn = get_connection()
    sns = get_sns_client()

    topics = get_topics_arns_from_aws(sns)
    tags = filter_topics(FILTER_TOPICS_BY, topics)

    tags_list = add_tags_to_dictionary(tags)
    logging.info("\nTags in AWS: %s\n", [tag['Tag'] for tag in tags_list])

    for tag_dict in tags_list:

        trending_albums = get_trending_items(conn, 'album', tag_dict['Tag'])
        trending_tracks = get_trending_items(conn, 'track', tag_dict['Tag'])
        trending_data = trending_tracks + trending_albums

        if len(trending_data) == 0:
            logging.info("No trending items found for %s \n",
                         tag_dict['Tag'])
            continue
        elif len(trending_data) >= 1:
            publish_list_to_topic(
                sns, tag_dict['TopicArn'], tag_dict['Tag'].title(), trending_data)
            logging.info("Email sent for %s \n",
                         tag_dict['Tag'])

    conn.close()


if __name__ == "__main__":
    configure_log()
    load_dotenv()

    logging.info("Notification system started.")

    notification_system()

    logging.info("Notification system ended.")
