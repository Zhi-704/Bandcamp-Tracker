"""Main script for running the ETL Pipeline."""

import logging
from dotenv import load_dotenv
from extract import get_sales_data
from transform import transform_sales_data
from load import load_sales_data


def main(event, context):
    """
    Main function to execute the ETL (Extract, Transform, Load) pipeline.

    - Configures logging with a warning level and a specific format.
    - Loads environment variables from a .env file using dotenv.
    - Fetches sales data using get_sales_data().
    - Transforms the fetched data using transform_sales_data().
    - Loads the transformed data into a database using load_sales_data().
    """

    logging.basicConfig(
        level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    try:
        load_dotenv()

        list_of_sales = get_sales_data()
        cleaned_sales = transform_sales_data(list_of_sales)
        load_sales_data(cleaned_sales)

    except Exception as e:
        logging.error("An error occurred during ETL pipeline execution: %s", e)
