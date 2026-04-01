## Configure logger instance for use throughout server

import logging
import sys

def setup_logging():

    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers = [logging.StreamHandler(sys.stdout)]
    )