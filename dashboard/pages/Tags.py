"""A dashboard page that lets you see sales by their tags."""

import streamlit as st

from database import get_connection, get_tag_sales_by_tag, get_all_tag_names
from charts import get_tag_sales_line_graph


def show_tags():
    st.title("Tags")
    conn = get_connection()

    all_tags = get_all_tag_names(conn)

    chosen_tag = st.selectbox(
        "Choose which tag you would like to see", all_tags)

    chosen_tag_data = get_tag_sales_by_tag(conn, chosen_tag)
    chosen_tag_data
    st.altair_chart(get_tag_sales_line_graph(chosen_tag_data))
