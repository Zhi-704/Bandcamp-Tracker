"""Functions for generating Altair chart visualisation used in dashboard."""

import altair as alt
import streamlit as st
from pandas import DataFrame
import plotly.express as px


@st.cache_data
def get_most_copies_sold_chart(data: DataFrame) -> alt.Chart:
    """Returns a bar chart of most copies sold when passed tracks/albums data."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("title", title="Title"),
        y=alt.Y("copies_sold:Q", title="Copies sold"),
        color=alt.Color("name", title="Artist")
    )


@st.cache_data
def get_most_popular_artists_chart(artists: DataFrame) -> alt.Chart:
    """Returns a bar chart of popular artists and their sales."""

    return alt.Chart(artists).mark_bar().encode(
        x=alt.X("name", title="Artists"),
        y=alt.Y("total_sales:Q", title="Sales")
    )


@st.cache_data
def get_most_popular_tags_chart(tags: DataFrame) -> alt.Chart:
    """Returns a bar chart of popular tags and their sales."""

    return alt.Chart(tags).mark_bar().encode(
        x=alt.X("tag", title="Tags"),
        y=alt.Y("total_sales:Q", title="Sales")
    )


@st.cache_data
def get_artist_stacked_chart(artists: DataFrame) -> alt.Chart:
    """Returns a bar chart showing split of albums vs. track sales for top artists"""

    return alt.Chart(artists).mark_bar().encode(
        x=alt.X("name", title="Artist"),
        y=alt.Y("total_sales:Q", title="Sales")
    )


@st.cache_data
def create_choropleth_map(locations):
    """Returns a global choropleth map by number of sales."""
    fig_map = px.choropleth(locations,
                            locations="name",
                            locationmode="country names",
                            color="total_sales",
                            hover_name="name",
                            hover_data="total_sales",
                            color_continuous_scale="Blues",
                            title="Sales",
                            labels={"total_sales": "Total sales", "name": "Country"})
    return fig_map


def get_albums_sales_line_graph(chosen_album) -> alt.Chart:
    """Returns a line graph of sales over time."""
    return alt.Chart(chosen_album).mark_line().encode(
        x=alt.X("timestamp:T"),
        y=alt.Y("sales:Q")
    )
