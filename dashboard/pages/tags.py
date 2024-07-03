"""A dashboard page that lets you see sales by their tags."""

import streamlit as st

from database import (
    get_connection,
    get_album_sales_by_tag,
    get_track_sales_by_tag,
    get_sales_by_tag,
    get_all_tags)
from charts import get_sales_line_graph, get_most_popular_tags_chart


def show_tags():
    """Main function for tags page."""
    st.title("Tags")
    conn = get_connection()

    all_tags = get_all_tags(conn)
    timeframe = st.radio(label="Filter by sale timeframe", options=[
        '1 day', '1 week', '1 month', "1 year"], horizontal=True)
    tags = get_sales_by_tag(conn, timeframe)

    st.subheader("Top Tags")
    st.altair_chart(get_most_popular_tags_chart(
        tags), use_container_width=True, )

    st.subheader("Tag popularity over time")
    chosen_tag = st.selectbox(
        "Choose which tag you would like to see...", all_tags)

    chosen_tag_album_data = get_album_sales_by_tag(conn, chosen_tag)
    chosen_tag_track_data = get_track_sales_by_tag(conn, chosen_tag)

    col = st.columns(2)

    with col[0]:
        st.subheader("Album sales")
        st.altair_chart(get_sales_line_graph(chosen_tag_album_data))
    with col[1]:
        st.subheader("Track sales")
        st.altair_chart(get_sales_line_graph(chosen_tag_track_data))
