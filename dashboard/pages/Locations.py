"""A dashboard page that lets you sign view sales by countries."""

import streamlit as st


from database import get_connection, get_sales_by_country
from charts import create_choropleth_map

if __name__ == "__main__":

    conn = get_connection()
    countries = get_sales_by_country(conn)
    st.plotly_chart(create_choropleth_map(countries))
    st.write("Note: Total sales is a combination of track and album purchases")
