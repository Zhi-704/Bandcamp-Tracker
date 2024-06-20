"""Main page of the dashboard."""


from dotenv import load_dotenv
import streamlit as st

from database import get_connection, get_popular_tracks, get_popular_albums, get_popular_artists, get_sales_by_tag
from charts import get_most_copies_sold_chart, get_most_popular_chart
if __name__ == "__main__":

    load_dotenv()

    conn = get_connection()

    st.title("Bandcamp sales analysis")

    tracks = get_popular_tracks(conn)
    albums = get_popular_albums(conn)
    artists = get_popular_artists(conn)
    # tags = get_sales_by_tag(conn)
    conn.close()
    tracks
    st.altair_chart(get_most_copies_sold_chart(
        tracks), use_container_width=True)
    st.altair_chart(get_most_copies_sold_chart(
        albums), use_container_width=True)
    st.altair_chart(get_most_popular_chart(artists), use_container_width=True)
    # tags
