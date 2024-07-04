"""Home page of the dashboard."""


import streamlit as st
import database
import charts


def show_home():
    """Main function for Home page."""

    conn = database.get_connection()
    conn = database.check_connection(conn)

    st.title("Home")
    col = st.columns(2)
    with col[0]:
        st.image('Apollo.png', use_column_width="auto")

        hide_img_fs = """
                    <style>
                    button[title="View fullscreen"]{
                        visibility: hidden;}
                    </style>
                    """

        st.markdown(hide_img_fs, unsafe_allow_html=True)
    with col[1]:
        st.header("Welcome to Apollo!")
        st.subheader("The Bandcamp Sales Tracker")
        st.write(
            """Here you'll find insights into Bandcamp sales and
            you can also subscribe to receive email notifications!""")
    timeframe = st.radio(label="Filter by sale timeframe", options=[
        '1 day', '1 week', '1 month', "1 year"], horizontal=True)
    st.header("Top tracks")

    st.write("Click on the bar to be taken to the relevant page on Bandcamp")
    tracks = database.get_popular_tracks(conn, timeframe=timeframe)
    st.altair_chart(charts.get_most_copies_sold_chart(
        tracks), use_container_width=True)

    st.header("Top albums")
    albums = database.get_popular_albums(conn, timeframe=timeframe)

    st.write("Click on the bar to be taken to the relevant page on Bandcamp")

    st.altair_chart(charts.get_most_copies_sold_chart(
        albums), use_container_width=True)
