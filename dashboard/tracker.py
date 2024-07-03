"""Navigation for dashboard."""
import os
from dotenv import load_dotenv
import streamlit as st
from streamlit_navigation_bar import st_navbar
import pages as pg


if __name__ == "__main__":
    st.set_page_config(page_title="Apollo", page_icon="Apollo.svg",
                       initial_sidebar_state="collapsed")
    load_dotenv()
    pages = ["Artists 🎤", "Locations 📍",
             "Subscriptions 📧", "Tags 🏷️"]
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(parent_dir, "Apollo.svg")
    options = {
        "show_menu": False,
        "show_sidebar": False,
    }
    page = st_navbar(pages, options=options, logo_path=logo_path)

    functions = {
        "Home": pg.show_home,
        "Artists 🎤": pg.show_artists,
        "Locations 📍": pg.show_locations,
        "Subscriptions 📧": pg.show_subscriptions,
        "Tags 🏷️": pg.show_tags,
    }
    go_to = functions.get(page)
    if go_to:
        go_to()
