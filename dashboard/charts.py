"""Functions for generating Altair chart visualisation used in dashboard."""

import altair as alt
import streamlit as st
from pandas import DataFrame


@st.cache_data
def get_most_copies_sold_chart(data: DataFrame) -> alt.Chart:
    """Returns a bar chart of most copies sold when passed tracks/albums data."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("title", title="Title"),
        y=alt.Y("copies_sold:N", title="Copies sold"),
        color=alt.Color("name", title="Artist")
    )


@st.cache_data
def get_most_popular_chart(data: DataFrame) -> alt.Chart:
    """Returns a bar chart of popular artists/tags and their sales."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("name", title="Artist"),
        y=alt.Y("total_sales:N", title="Sales")
    )


def get_artist_stacked_chart(artists: DataFrame) -> alt.Chart:
    """Returns a bar chart showing split of albums vs. track sales for top artists"""

    return alt.Chart(artists).mark_bar().encode(
        x=alt.X("name", title="Artist"),
        y=alt.Y("total_sales:N", title="Sales")
    )
