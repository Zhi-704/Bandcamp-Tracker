"""A dashboard page that lets you view sales by track vs. albums for top artists."""

import streamlit as st

from database import get_connection, get_popular_artists, get_all_artists, get_sales_by_artist
from charts import get_artist_album_sales_bar_chart, get_artist_track_sales_bar_chart, get_most_popular_artists_chart

if __name__ == "__main__":

    conn = get_connection()
    pop_artists = get_popular_artists(conn)
    st.altair_chart(get_most_popular_artists_chart(
        pop_artists), use_container_width=True)

    all_artists = get_all_artists(conn)
    chosen_artists = st.multiselect(
        "Choose which artist you would like to see", all_artists, max_selections=2)
    if len(chosen_artists) == 2:

        chosen_artists_data = get_sales_by_artist(conn, chosen_artists)
        chosen_artists_data
        col = st.columns(2)
        with col[0]:
            st.altair_chart(
                get_artist_album_sales_bar_chart(chosen_artists_data))

        with col[1]:
            st.altair_chart(
                get_artist_track_sales_bar_chart(chosen_artists_data))
