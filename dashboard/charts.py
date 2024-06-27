"""Functions for generating Altair chart visualisation used in dashboard."""

import altair as alt
import streamlit as st
from pandas import DataFrame
import plotly.express as px

BANDCAMP_BLUE = "rgb(60, 154, 170)"


@st.cache_data
def get_most_copies_sold_chart(data: DataFrame) -> alt.Chart:
    """Returns a bar chart of most copies sold when passed tracks/albums data."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("title", title="Title", axis=alt.Axis(
            labelAngle=-45)).sort("-y"),
        y=alt.Y("copies_sold:Q", title="Copies sold"),
        color=alt.Color("name", title="Artist"),
        href="url:N"
    )


@st.cache_data
def get_most_popular_artists_chart(artists: DataFrame) -> alt.Chart:
    """Returns a bar chart of popular artists and their sales."""

    return alt.Chart(artists).mark_bar().encode(
        x=alt.X("name:N", title="Artists",
                axis=alt.Axis(labelAngle=-45)).sort("-y"),
        y=alt.Y("total_sales:Q", title="Sales"),
        color=alt.Color("name:N", title="Artist"),
        href="artist_url:N"

    )


@st.cache_data
def get_most_popular_tags_chart(tags: DataFrame) -> alt.Chart:
    """Returns a bar chart of popular tags and their sales."""
    tags["total_sales"] = tags["total_sales"].astype(int)
    return alt.Chart(tags).mark_bar(color=BANDCAMP_BLUE).encode(
        x=alt.X("name:N", title="Tags", axis=alt.Axis(
            labelAngle=-45)).sort("-y"),
        y=alt.Y("total_sales:Q", title="Sales")
    )


@st.cache_data
def get_artist_track_sales_bar_chart(artists: DataFrame) -> alt.Chart:
    """Returns a bar chart showing track sales for top artists"""

    return alt.Chart(artists).mark_bar(color=BANDCAMP_BLUE).encode(
        x=alt.X("name:N", title="Artist", axis=alt.Axis(
            labelAngle=-45)).sort("-y"),
        y=alt.Y("track_sales:Q", title="Tracks sold")
    )


@st.cache_data
def get_artist_album_sales_bar_chart(artists: DataFrame) -> alt.Chart:
    """Returns a bar chart showing split of albums sales for top artists"""

    return alt.Chart(artists).mark_bar(color=BANDCAMP_BLUE).encode(
        x=alt.X("name:N", title="Artist", axis=alt.Axis(
            labelAngle=-45)).sort("-y"),
        y=alt.Y("album_sales:Q", title="Albums sold")

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


@st.cache_data
def get_albums_sales_line_graph(chosen_album) -> alt.Chart:
    """Returns a line graph of sales over time for a chosen album."""
    return alt.Chart(chosen_album).mark_line().encode(
        x=alt.X("timestamp:T"),
        y=alt.Y("sales:Q"),
        color="name:N"
    ).interactive()


@st.cache_data
def get_tag_sales_line_graph(chosen_tag) -> alt.Chart:
    """Returns a line graph of sales over time for a chosen tag"""
    return alt.Chart(chosen_tag).mark_line(point=True, color=BANDCAMP_BLUE).encode(
        x=alt.X("hour:T"),
        y=alt.Y("sales:Q")
    ).interactive()
