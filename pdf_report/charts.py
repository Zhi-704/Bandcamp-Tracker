import altair as alt
import streamlit as st
from pandas import DataFrame


def get_top_artists_chart(data: DataFrame) -> alt.Chart:
    """Returns a bar chart of top 5 selling artists."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("2:N", title="Artists"),
        y=alt.Y("1:Q", title="Sales (USD)")
    )


def get_top_tags_chart(data: DataFrame) -> alt.Chart:
    """Returns a bar chart of top 5 selling tags."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("2:N", title="Tags"),
        y=alt.Y("1:Q", title="Sales (USD)")
    )


def get_top_tracks_chart(data: DataFrame) -> alt.Chart:
    """Returns a bar chart of top 5 selling tracks."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("2:N", title="Tracks"),
        y=alt.Y("1:Q", title="Sales (USD)")
    )
