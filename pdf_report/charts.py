"""
This script is dedicated to using altair to create bar charts to aid with the
visualistions of the PDF. Each function creates a different bar chart for the data
that is provided for it.
"""


import altair as alt
from pandas import DataFrame


def get_top_artists_chart(data: DataFrame) -> alt.Chart:
    """Returns an altair bar chart of top 5 selling artists."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("2:N", axis=alt.Axis(title="Artists", labels=False)),
        y=alt.Y("1:Q", title="Sales (USD)"),
        color=alt.Color("2:N", scale=alt.Scale(
            scheme="blues"), legend=alt.Legend(title="Artists"))
    ).properties(
        width=60,
        height=145,
    )


def get_top_tags_chart(data: DataFrame) -> alt.Chart:
    """Returns an altair bar chart of top 5 selling tags."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("2:N", axis=alt.Axis(title="Tags", labels=False)),
        y=alt.Y("1:Q", title="Sales (USD)"),
        color=alt.Color("2:N", scale=alt.Scale(
            scheme="blues"), legend=alt.Legend(title="Tags"))
    ).properties(
        width=62,
        height=145,
    )


def get_top_tracks_chart(data: DataFrame) -> alt.Chart:
    """Returns an altair bar chart of top 5 selling tracks."""

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("2:N", axis=alt.Axis(title="Tracks", labels=False)),
        y=alt.Y("1:Q", title="Sales (USD)"),
        color=alt.Color("2:N", scale=alt.Scale(
            scheme="blues"), legend=alt.Legend(title="Tracks"))
    ).properties(
        width=60,
        height=145,
    )
