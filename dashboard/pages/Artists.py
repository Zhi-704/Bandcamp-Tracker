"""A dashboard page that lets you view sales by track vs. albums for top artists."""

import streamlit as st

from database import get_connection, get_popular_artists, get_all_artists, get_sales, get_sales_for_chosen_artists
from charts import get_artist_album_sales_bar_chart, get_artist_track_sales_bar_chart, get_most_popular_artists_chart

if __name__ == "__main__":

    conn = get_connection()
    pop_artists = get_popular_artists(conn)
    pop_artists
    st.altair_chart(get_most_popular_artists_chart(
        pop_artists), use_container_width=True)

    all_artists = get_all_artists(conn)
    chosen_artists = st.multiselect(
        "Choose artists to compare their track vs. album sales", all_artists, placeholder="Choose artists...")
    all_sales = get_sales(conn)
    chosen_artists_data = get_sales_for_chosen_artists(
        all_sales, chosen_artists)
    col = st.columns(2)
    with col[0]:
        st.altair_chart(
            get_artist_album_sales_bar_chart(chosen_artists_data))

    with col[1]:
        st.altair_chart(
            get_artist_track_sales_bar_chart(chosen_artists_data))
