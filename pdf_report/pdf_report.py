"""Main script for generating the daily report PDF and mailing it to all subscribers."""

import logging
from generate_pdf import create_pdf
from mailer import send_all_emails


def main(event, context):  # pylint: disable=unused-argument
    """Main function to execute the:
        1. Generation of the daily report PDFs
        2. Sending of PDFs to all subscribers
    """

    logging.basicConfig(
        level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    create_pdf()
    send_all_emails()


if __name__ == "__main__":
    main("foo", "bar")
