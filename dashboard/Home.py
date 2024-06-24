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
    tags = database.get_sales_by_tag(conn)
    st.altair_chart(charts.get_most_copies_sold_chart(
        tracks), use_container_width=True)
    st.altair_chart(charts.get_most_copies_sold_chart(
        albums), use_container_width=True)
    st.altair_chart(charts.get_most_popular_tags_chart(
        tags), use_container_width=True)

    # chosen_album = st.selectbox(
    #     "Choose which album you would like to see", album_titles)

    # chosen_album_data = database.get_album_sales_by_album(conn, chosen_album)
    # chosen_album_data
    # st.altair_chart(charts.get_albums_sales_line_graph(chosen_album_data))
