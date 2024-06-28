"""Home page of the dashboard."""


import streamlit as st
import database
import charts


def show_home():
    """Main function for Home page."""

    conn = database.get_connection()

    st.title("Home")
    col = st.columns(2)
    with col[0]:
        st.image('Apollo.png', use_column_width="auto")
    with col[1]:
        st.header("Welcome to Apollo!")
        st.subheader("The Bandcamp Sales Tracker")
        st.write(
            """Here you'll find insights into Bandcamp sales and
            you can also subscribe to receive email notifications!""")

    tracks = database.get_popular_tracks(conn)
    albums = database.get_popular_albums(conn)
    st.subheader("Top Tracks")
    st.write("Click on the bar to be taken to the relevant page on Bandcamp")

    st.altair_chart(charts.get_most_copies_sold_chart(
        tracks), use_container_width=True)
    st.subheader("Top Albums")
    st.write("Click on the bar to be taken to the relevant page on Bandcamp")

    st.altair_chart(charts.get_most_copies_sold_chart(
        albums), use_container_width=True)
