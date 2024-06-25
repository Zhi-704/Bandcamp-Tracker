"""A dashboard page that lets you sign up for notifications."""

import streamlit as st


from database import get_all_tags, get_connection


def show_subscriptions():

    st.page_link("./Home.py", label="Home")

    email = ""
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
            tag = st.multiselect(
                "Choose which tag(s) you would like to subscribe to",
                get_all_tags(conn),
                placeholder="Select tag...")
            if not tag:
                st.error("Missing field - you must choose at least one tag")
        st.form_submit_button()

    if email and len(tag) == 1:
        st.write(f"You are now subscribed to the {tag[0]} tag")
        # add similar message as above for subscribing to multiple tags
