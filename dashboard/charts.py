"""charts used in dashboard"""

import altair as alt
import streamlit as st
from pandas import DataFrame


@st.cache_data(ttl="1hr")
def get_most_copies_sold_chart(data: DataFrame) -> alt.Chart:
    """Returns a bar chart of most copies sold when passed tracks/albums data."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("title"),
        y=alt.Y("copies_sold:N")
    )


@st.cache_data(ttl="1hr")
def get_popular_artists_chart(artists: DataFrame) -> alt.Chart:
    """Returns a bar chart of popular artists and their sales."""

    return alt.Chart(artists).mark_bar().encode(
        x=alt.X("name"),
        y=alt.Y("total_sales:N")
    )


@st.cache_data(ttl="1hr")
def top_tags_chart(tags: DataFrame) -> alt.Chart:
    """Returns a bar chart of popular tags and their sales."""

    return alt.Chart(tags).mark_bar().encode(
        x=alt.X("name"),
        y=alt.Y("sales:N")
    )
