"""Home page of the dashboard."""


from dotenv import load_dotenv
import streamlit as st
import database
import charts


def show_home():
    """Main function for Home page."""

    conn = database.get_connection()

    st.title("Home")
    st.header("Welcome to the Bandcamp analysis tracker!")
    st.write("Here you'll find insights into Bandcamp sales and you can also subscribe to receive email notifications!")
    album_titles = database.get_all_album_titles(conn)

    tracks = database.get_popular_tracks(conn)
    albums = database.get_popular_albums(conn)
    st.subheader("Top Tracks")
    st.altair_chart(charts.get_most_copies_sold_chart(
        tracks), use_container_width=True)
    st.subheader("Top Albums")
    st.altair_chart(charts.get_most_copies_sold_chart(
        albums), use_container_width=True)

    chosen_album = st.selectbox(
        "Choose which album you would like to see", album_titles)
