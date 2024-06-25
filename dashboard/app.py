"""Main page of the dashboard."""


import streamlit as st
from streamlit_navigation_bar import st_navbar
import pages as pg


if __name__ == "__main__":
    st.set_page_config(initial_sidebar_state="collapsed")
    pages = ["Home", "Artists", "Locations", "Subscriptions", "Tags"]
    page = st_navbar(pages)

    functions = {
        "Home": pg.show_home,
        "Artists": pg.show_artists,
        "Locations": pg.show_locations,
        "Subscriptions": pg.show_subscriptions,
        "Tags": pg.show_tags,
    }
    go_to = functions.get(page)
    if go_to:
        go_to()
