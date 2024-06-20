"""A dashboard page that lets you sign view sales by countries."""

import streamlit as st

from database import get_connection, get_sales_by_country
from charts import create_choropleth_map
conn = get_connection()
countries = get_sales_by_country(conn)
st.plotly_chart(create_choropleth_map(countries))
