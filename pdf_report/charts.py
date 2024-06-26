import altair as alt
import streamlit as st
from pandas import DataFrame


def get_top_artists_chart(data: DataFrame) -> alt.Chart:
    """Returns a bar chart of top 5 selling artists."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("artist:N", title="Artists", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("total_sales:Q", title="Total Sales")
    )


def get_top_genres_chart(data: DataFrame) -> alt.Chart:
    """Returns a bar chart of top 5 selling tags."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("tag:N", title="Tags", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("total_sales:Q", title="Total Sales")
    )


def get_top_tracks_chart(data: DataFrame) -> alt.Chart:
    """Returns a bar chart of top 5 selling tracks."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("track:N", title="Tracks", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("total_sales:Q", title="Total Sales")
    )
