"""A dashboard page that lets you sign view sales by countries."""

import streamlit as st


from database import get_connection, check_connection, get_sales_by_country
from charts import create_choropleth_map


def show_locations():
    """Main function for Locations page."""
    st.title("Locations")
    st.write("Hover to see the number of sales made in each country")
    conn = get_connection()
    conn = check_connection(conn)
    countries = get_sales_by_country(conn)
    st.plotly_chart(create_choropleth_map(countries))
    st.write("Note: Total sales is a combination of track and album purchases")
