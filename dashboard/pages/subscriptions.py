"""A dashboard page that lets you sign up for notifications."""

from os import environ as ENV
import streamlit as st
import boto3
from database import get_all_tags, get_connection

ARN_PREFIX = "arn:aws:sns:eu-west-2:129033205317:c11-bandcamp"

TOPIC_NAME_ALLOWED = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-"


def create_subscription(protocol, endpoint, arn, client):
    """Adds a subscription to a topic"""
    return client.subscribe(TopicArn=arn, Protocol=protocol, Endpoint=endpoint)


def create_topic(client, topic_name: str):
    """Creates an sns topic"""
    client.create_topic(
        Name=f"c11-bandcamp-{topic_name}",
    )


def get_topics(client):
    """Returns a list of all sns topics"""
    response = client.list_topics()
    topics = response["Topics"]
    return [topic["TopicArn"] for topic in topics]


def show_subscriptions():
    """Displays the subscription page and runs the processes
        responsible for managing subscriptions."""
    st.title("Subscriptions")

    conn = get_connection()

    st.write("We offer two different email subscriptions:")
    st.write(
        "1. PDF reports - daily summaries of purchases on Bandcamp as a PDF emailed to you")
    pdf = st.checkbox(
        "I would like to sign up for daily PDF reports")
    st.write(
        "2. Notifications - get notified of what's trending for your favourite tags!")
    notifications = st.checkbox(
        "I would like to sign up for notifications for specific tags"
    )

    email = None
    tags = None

    with st.form(
        "Subscriptions",
        clear_on_submit=False,
        border=True,
    ):
        st.header("Subscribe to emails")

        email = st.text_input("Email")
        if pdf:
            name = st.text_input("Name")
        if notifications:
            tags = st.multiselect(
                "Choose which tag(s) you would like to subscribe to...",
                get_all_tags(conn),
                placeholder="Select tag...",
            )

        submitted = st.form_submit_button()

        if submitted:
            if pdf and not name:
                st.error("Missing field - you must enter a 'Name'")
            if not email:
                st.error("Missing field - you must enter an 'Email'")
            if email and "@" not in email:
                st.error("Invalid email")
            if notifications and not tags:
                st.error("Missing field - you must choose at least one tag")

    sns_client = boto3.client(
        "sns",
        region_name="eu-west-2",
        aws_access_key_id=ENV["ACCESS_KEY"],
        aws_secret_access_key=ENV["SECRET_ACCESS_KEY"],
    )
    topic_arns = get_topics(sns_client)

    if submitted:
        if notifications and email and tags:
            st.write(f"You are now subscribed to the {tags} tag(s)")
            for tag in tags:
                tag = tag.replace(" ", "-")
                if (
                    f"{ARN_PREFIX}-{tag}"
                    not in topic_arns
                ):
                    for char in tag:
                        if char not in TOPIC_NAME_ALLOWED:
                            tag = tag.replace(char, "_")
                    create_topic(sns_client, tag)
                    create_subscription(
                        "email",
                        email,
                        f"{ARN_PREFIX}-{
                            tag}",
                        sns_client,
                    )

                else:
                    topic_arn = f"{ARN_PREFIX}-{
                        tag}"
                    create_subscription("email", email, topic_arn, sns_client)

        if pdf and name and email:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO subscriber (email, name) VALUES (%s, %s)""",
                    (email, name),
                )
            conn.commit()
            st.write("You are now subscribed to receive daily PDF reports")
