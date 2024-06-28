"""A dashboard page that lets you view sales by track vs. albums for artists."""

import streamlit as st

from database import (
    get_connection,
    get_popular_artists,
    get_all_artists,
    get_sales,
    get_sales_for_chosen_artists,
    get_track_sales_by_artist,
    get_album_sales_by_artist
)
from charts import (
    get_artist_album_sales_bar_chart,
    get_artist_track_sales_bar_chart,
    get_most_popular_artists_chart,
    get_sales_line_graph
)


def show_artists():
    """Displays the page showing visualisations relating to artists."""
    st.title("Artists")
    conn = get_connection()
    timeframe = st.radio(label="Filter by sale timeframe", options=[
        '1 day', '1 week', '1 month', "1 year"], horizontal=True)

    pop_artists = get_popular_artists(conn, timeframe)
    st.header("Top Artists")
    st.write("Click on the bar to be taken to the relevant page on Bandcamp")

    st.altair_chart(
        get_most_popular_artists_chart(pop_artists), use_container_width=True
    )

    all_artists = get_all_artists(conn)
    chosen_artists = st.multiselect(
        "Choose artists to compare their track vs. album sales",
        all_artists,
        placeholder="Choose artists...",
    )
    all_sales = get_sales(conn)
    chosen_artists_data = get_sales_for_chosen_artists(
        all_sales, chosen_artists)
    if chosen_artists:
        st.altair_chart(
            get_artist_album_sales_bar_chart(chosen_artists_data),
            use_container_width=True,
        )

        st.altair_chart(
            get_artist_track_sales_bar_chart(chosen_artists_data),
            use_container_width=True,
        )

    one_artist = st.selectbox("Choose artist", all_artists)
    chosen_artists_track_data = get_track_sales_by_artist(conn, one_artist)
    chosen_artists_album_data = get_album_sales_by_artist(conn, one_artist)
    cols = st.columns(2)
    if one_artist:
        with cols[0]:
            st.subheader("Track sales")
            st.altair_chart(get_sales_line_graph(chosen_artists_track_data))
        with cols[1]:
            st.subheader("Album sales")
            st.altair_chart(get_sales_line_graph(chosen_artists_album_data))
