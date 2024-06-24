"""A dashboard page that lets you sign up for notifications."""
from database import get_all_tags, get_connection
import streamlit as st
import boto3
from os import environ as ENV
from dotenv import load_dotenv


# Function to create a subscription
def create_subscription(protocol, endpoint, topic_arn):
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol=protocol,
        Endpoint=endpoint
    )
    return response


def create_topic(topic_name: str):
    response = sns_client.create_topic(
        Name=f"c11-bandcamp-{topic_name}-tag",
    )


if __name__ == "__main__":
    load_dotenv()

    st.page_link("./Home.py", label="Home")

    conn = get_connection()

    st.write(
        "PDF reports: daily summaries of purchases on bandcamp as a PDF emailed to you")
    st.write("Notifications: ")

    pdf = st.checkbox("I would like to sign up for daily PDF reports")
    notifications = st.checkbox(
        "I would like to sign up for notifications for specific tags")

    with st.form("Subscriptions", clear_on_submit=False, border=True):
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
                "Choose which tag(s) you would like to subscribe to",
                get_all_tags(conn),
                placeholder="Select tag...")
            if not tags:
                st.error("Missing field - you must choose at least one tag")
        st.form_submit_button()

    if email and len(tags) == 1:
        st.write(f"You are now subscribed to the {tags[0]} tag")
        # add similar message as above for subscribing to multiple tags

    if pdf and name:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO subscriber (email, name) VALUES (%s, %s)""", (email, name))
        conn.commit()

    sns_client = boto3.client(
        'sns',
        region_name='eu-west-2',
        aws_access_key_id=ENV["ACCESS_KEY"],
        aws_secret_access_key=ENV["SECRET_ACCESS_KEY"]
    )
    response = sns_client.list_topics()
    topics = response["Topics"]
    topic_arns = [topic["TopicArn"] for topic in topics]

    if notifications and tags:
        for tag in tags:
            if f'arn:aws:sns:eu-west-2:129033205317:c11-bandcamp-{tag}-tag' not in topic_arns:
                create_topic(tag)
                create_subscription(
                    'email', email, f'arn:aws:sns:eu-west-2:129033205317:c11-bandcamp-{tag}-tag')

            else:
                topic_arn = f'arn:aws:sns:eu-west-2:129033205317:c11-bandcamp-{
                    tag}-tag'
                create_subscription('email', email, topic_arn)
