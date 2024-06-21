"""Main page of the dashboard."""


from dotenv import load_dotenv
import streamlit as st

from database import get_connection, get_popular_tracks, get_popular_albums, get_popular_artists, get_sales_by_tag, get_sales_by_country, get_album_sales_by_album, get_all_album_titles
from charts import get_most_copies_sold_chart, get_most_popular_artists_chart, get_most_popular_tags_chart, create_choropleth_map, get_albums_sales_line_graph
if __name__ == "__main__":

    load_dotenv()

    conn = get_connection()

    st.title("Bandcamp sales analysis")
    album_titles = get_all_album_titles(conn)
    album_titles

    tracks = get_popular_tracks(conn)
    albums = get_popular_albums(conn)
    artists = get_popular_artists(conn)
    tags = get_sales_by_tag(conn)

    # specific_album = get_album_sales_by_album(conn)
    st.altair_chart(get_most_copies_sold_chart(
        tracks), use_container_width=True)
    st.altair_chart(get_most_copies_sold_chart(
        albums), use_container_width=True)
    st.altair_chart(get_most_popular_artists_chart(
        artists), use_container_width=True)
    st.altair_chart(get_most_popular_tags_chart(
        tags), use_container_width=True)

    chosen_album = st.selectbox(
        "Choose which album you would like to see", get_all_album_titles(conn))

    chosen_album_data = get_album_sales_by_album(conn, chosen_album)
    chosen_album_data
    st.altair_chart(get_albums_sales_line_graph(chosen_album_data))
