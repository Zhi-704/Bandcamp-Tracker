"""A dashboard page that lets you sign up for notifications."""

from os import environ as ENV
import streamlit as st
import boto3
from dotenv import load_dotenv
from database import get_all_tags, get_connection


def create_subscription(protocol, endpoint, arn):
    """Adds a subscription to a topic"""
    return sns_client.subscribe(
        TopicArn=arn,
        Protocol=protocol,
        Endpoint=endpoint
    )


def create_topic(topic_name: str):
    """creates an sns topic"""
    sns_client.create_topic(
        Name=f"c11-bandcamp-{topic_name}",
    )


def get_topics(client):
    """returns a list of all sns topics"""
    response = client.list_topics()
    topics = response["Topics"]
    return [topic["TopicArn"] for topic in topics]


if __name__ == "__main__":
    load_dotenv()

    st.page_link("./Home.py", label="Home")

    conn = get_connection()

    st.write("We offer two different subscriptions:")
    st.write(
        "1. PDF reports - daily summaries of purchases on Bandcamp as a PDF emailed to you")
    st.write(
        "2. Notifications - get notified of what's trending for your favourite tags!")

    pdf = st.checkbox(
        "I would like to sign up for daily PDF reports")
    notifications = st.checkbox(
        "I would like to sign up for notifications for specific tags")

    email = None
    tags = None

    with st.form("Subscriptions", clear_on_submit=False, border=True, ):
        st.header("Subscribe to emails")
        if pdf:
            name = st.text_input("Name")
        if pdf and not name:
            st.error("Missing field - you must enter a 'Name'")
        email = st.text_input("Email")
        if not email:
            st.error("Missing field - you must enter an 'Email'")
        if email and "@" not in email:
            st.error("Invalid email")

        if notifications:
            tags = st.multiselect(
                "Choose which tag(s) you would like to subscribe to...",
                get_all_tags(conn),
                placeholder="Select tag...")
            if not tags:
                st.error("Missing field - you must choose at least one tag")
        submitted = st.form_submit_button()

    sns_client = boto3.client(
        'sns',
        region_name='eu-west-2',
        aws_access_key_id=ENV["ACCESS_KEY"],
        aws_secret_access_key=ENV["SECRET_ACCESS_KEY"]
    )
    topic_arns = get_topics(sns_client)

    if submitted:
        if notifications and email and tags:
            st.write(f"You are now subscribed to the {tags} tag(s)")
            for tag in tags:
                tag = tag.replace(" ", "-")
                if f'arn:aws:sns:eu-west-2:129033205317:c11-bandcamp-{tag}' not in topic_arns:
                    create_topic(tag)
                    create_subscription(
                        'email', email, f'arn:aws:sns:eu-west-2:129033205317:c11-bandcamp-{tag}')

                else:
                    topic_arn = f'arn:aws:sns:eu-west-2:129033205317:c11-bandcamp-{
                        tag}'
                    create_subscription('email', email, topic_arn)

        if pdf and name and email:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO subscriber (email, name) VALUES (%s, %s)""", (email, name))
            conn.commit()
            st.write("You are now subscribed to receive daily PDF reports")
