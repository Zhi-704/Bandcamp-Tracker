"""A dashboard page that lets you sign up for notifications."""

import streamlit as st

from database import get_all_tags, get_connection

if __name__ == "__main__":

    st.page_link("./Home.py", label="Home")

    email = ""
    age = ""
    conn = get_connection()
    col = st.columns(2)

    with col[0]:
        with st.form("notification-subscription", clear_on_submit=True, border=True):
            st.header("Subscribe to email notifications by tag")
            email = st.text_input("Email")
            if not email:
                st.error("Missing field - you must enter an 'Email'")
            if email and "@" not in email:
                st.error("Invalid email")
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
    with col[1]:
        with st.form("pdf-subscription", clear_on_submit=True, border=True):
            st.header("Subscribe to daily summary PDF reports")
            name = st.text_input("Name")
            if not name:
                st.error("Missing field - you must enter a 'Name'")
            email = st.text_input("Email")
            if not email:
                st.error("Missing field - you must enter an 'Email'")
            if email and "@" not in email:
                st.error("Invalid email")
            st.form_submit_button()
