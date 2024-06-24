"""Main page of the dashboard."""


from dotenv import load_dotenv
import streamlit as st

import database
import charts

if __name__ == "__main__":

    load_dotenv()

    conn = database.get_connection()

    st.title("Bandcamp sales analysis")
    album_titles = database.get_all_album_titles(conn)

    tracks = database.get_popular_tracks(conn)
    albums = database.get_popular_albums(conn)
    artists = database.get_popular_artists(conn)
    tags = database.get_sales_by_tag(conn)

    st.altair_chart(charts.get_most_copies_sold_chart(
        tracks), use_container_width=True)
    st.altair_chart(charts.get_most_copies_sold_chart(
        albums), use_container_width=True)
    st.altair_chart(charts.get_most_popular_artists_chart(
        artists), use_container_width=True)
    st.altair_chart(charts.get_most_popular_tags_chart(
        tags), use_container_width=True)
