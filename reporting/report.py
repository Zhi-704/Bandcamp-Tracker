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


def get_popular_tracks(_conn: Connection,
                       n: int = 5,
                       genre: str = "") -> pd.DataFrame:
    """Returns the N most sold tracks in the database."""

    print("Collating most popular tracks...")

    query = """
        SELECT T.title, A.name as band, COUNT(*) AS copies_sold
        FROM track_purchase AS PT
        JOIN track AS T USING(track_id)
        JOIN artist as A USING(artist_id)
        GROUP BY T.title, A.name
        ORDER BY copies_sold DESC
        LIMIT %s
        ;
        """

    with _conn.cursor() as cur:
        cur.execute(query, (n,))
        data = cur.fetchall()
    print(data)
    return pd.DataFrame(data)


def filter_topics(filter: str, topic_list: list[dict]) -> list[dict]:
    '''Filters list of topics with relevant topics'''
    return [topic for topic in topic_list if filter in topic['TopicArn']]


def get_list_of_tags_arn(sns_client: client) -> list[dict]:
    '''Gets all available topics on AWS'''
    response = sns_client.list_topics()
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Topics']
    return None


if __name__ == "__main__":
    load_dotenv()
    # conn = get_connection()
    # df = get_popular_tracks(conn)
    # conn.close()
    # print(df.head())
    sns_client = get_sns_client()
    topics = get_list_of_tags_arn(sns_client)
    tag_topics = filter_topics('apollo', topics)
    test_arn = tag_topics[0]['TopicArn']
    sub = sns_client.list_subscriptions_by_topic(
        TopicArn=test_arn
    )
    print(sub['Subscriptions'])
