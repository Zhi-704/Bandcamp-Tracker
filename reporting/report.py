from os import environ as ENV
from dotenv import load_dotenv
import pandas as pd

from psycopg import connect, Connection
from psycopg.rows import dict_row
from boto3 import client

'''
it sends messages to the topic
use a boto3 function to retrieve a function of all those tags
Iterate over those tags to see an album/track is trending under that tag (NO ARTIST)
Could do that they subscribe to an artist?
If they are, push a message to the topic
'''

TRENDING_THRESHOLD = 100
FILTER_GROUP = "c11-apollo-"


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
    '''Filters list of topics with relevant topics'''
    return [topic for topic in topic_list if filter_word in topic['TopicArn']]


def get_list_of_tags_arn(sns_client: client) -> list[dict]:
    '''Gets all available topics on AWS'''
    response = sns_client.list_topics()
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Topics']
    return None


def publish_to_topic(sns_client: client, topic_arn: str,  tag: str, item_name: str, item_author: str, item_type: str, item_url: str) -> dict:
    '''Publishes a message to a topic, which sends an email to all subscribers'''

    subject = f"New trending {item_type} for {tag}!"
    message = f"The {item_type} '{item_name}' by '{
        item_author}' is currently trending!\n"
    message += f"Check it out here at: {item_url}"

    response = sns_client.publish(
        TopicArn=topic_arn,
        Subject=subject,
        Message=message,
    )
    return response


def get_tag_arn(tag: str, arn_list: list[dict]) -> list[str]:
    '''Get the arn of a specific tag if it exists'''
    return [arn['TopicArn'] for arn in arn_list if tag in arn['TopicArn']]


def get_sales_data_of_tag(conn: Connection, item_type: str, tag: str, sales_limit: int = TRENDING_THRESHOLD) -> list[dict]:
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
GROUP BY
    T.{item_type}_id,
    T.title,
    A.name
HAVING COUNT(DISTINCT TP.{item_type}_purchase_id) >= %s
ORDER BY copies_sold DESC
'''

    with conn.cursor() as cur:
        cur.execute(query, (tag, sales_limit))
        trending_data = cur.fetchall()

    if len(trending_data) >= 1:
        return trending_data
    return None


def get_all_tags(conn: Connection) -> list[str]:
    query = '''
    SELECT name
    FROM tag;'''
    with conn.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()
    return [tag['name'] for tag in data]


def extract_tag_name(topic_arn: str) -> str:
    return topic_arn.split('-')[-1]


if __name__ == "__main__":
    load_dotenv()

    conn = get_connection()
    sns = get_sns_client()

    topics = get_list_of_tags_arn(sns)
    tags_list = filter_topics('apollo', topics)

    for tag_arn in tags_list:
        topic_arn = tag_arn['TopicArn']
        tag_name = extract_tag_name(topic_arn)
        tag_arn['Tag'] = tag_name

    print(tags_list)

    for tag_dict in tags_list:
        trending_albums = get_sales_data_of_tag(
            conn, 'album', tag_dict['Tag'], 3)
        trending_tracks = get_sales_data_of_tag(
            conn, 'track', tag_dict['Tag'], 3)
        print(f"Trending album ({tag_dict['Tag']}) : ", trending_albums)
        print(f"Trending track ({tag_dict['Tag']}) : ", trending_tracks)

        if trending_albums:
            for album in trending_albums:
                publish_to_topic(sns, tag_dict['TopicArn'],
                                 tag_dict['Tag'], album['title'], album['band'], 'album', album['url'])

        if trending_tracks:
            for track in trending_tracks:
                publish_to_topic(sns, tag_dict['TopicArn'],
                                 tag_dict['Tag'], track['title'], track['band'], 'track', track['url'])

    conn.close()
