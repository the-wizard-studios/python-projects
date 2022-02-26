import os
import logging
import datetime


# - Global Variables - #
log = ""

# Current Script Name
CURRENT_SCRIPT_NAME = os.path.basename(__file__).split('.')[0]

# Directories
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
LOGS_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "Logs")


# Logger
def logger():

    global log

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    # Formatter => Date/Time : Log Level : File Name : Function Name : Line Number : Message
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(filename)s : %(funcName)s : %(lineno)d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

    # Current Year-Month
    current_year_month = datetime.datetime.now().strftime("%Y-%m")

    # Logger file name
    log_file_name = f"{current_year_month}_{CURRENT_SCRIPT_NAME}.log"

    # Create Logs Folder if it does not exist
    os.makedirs(LOGS_DIRECTORY, exist_ok=True)

    # Log file path
    log_file = os.path.join(LOGS_DIRECTORY, log_file_name)

    # File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    # StreamHandler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)


# Hello
def hello():
    log.debug("Hello World")


# Main
if __name__ == "__main__":
    logger()

    log.debug("--- Start ---")

    log.debug("Custom Logger")

    # Hello
    hello()

    log.debug("--- End ---")
