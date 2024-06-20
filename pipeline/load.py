"""Script containing functions for loading sales data into the Database."""

from os import environ as ENV
import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection, cursor


def get_connection() -> connection:
    """ Creates a database session and returns a connection object """
    return psycopg2.connect(
        database=database_name,
        user=database_username,
        host=database_ip,
        password=database_password,
        port=database_port
    )
