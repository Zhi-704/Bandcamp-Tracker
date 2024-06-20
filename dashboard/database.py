"""Functions for interacting with the database."""

from os import environ as ENV

from psycopg import connect, Connection
from psycopg.rows import dict_row
from dotenv import load_dotenv
import streamlit as st
import pandas as pd


@st.cache_resource
def get_connection() -> Connection:
    """gets a connection"""
    connection = connect(
        port=ENV["DB_PORT"],
        dbname=ENV["DB_NAME"],
        host=ENV["DB_ENDPOINT"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"]
    )
    return connection


if __name__ == "__main__":
    load_dotenv()
    get_connection()
