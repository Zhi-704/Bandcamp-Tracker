"""Main script for running the ETL Pipeline."""

from dotenv import load_dotenv
from extract import get_sales_data
from transform import transform_sales_data
from load import load_sales_data
import logging
import time

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    while True:
        try:

            load_dotenv()

            list_of_sales = get_sales_data()
            cleaned_sales = transform_sales_data(list_of_sales)
            load_sales_data(cleaned_sales)
        except Exception as e:
            logging.error("An error occurred during the ETL process: %s", e)
        time.sleep(120)  # Sleep for 2 minutes
