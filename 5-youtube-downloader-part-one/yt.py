import os
import logging
import datetime
from pytube import YouTube # pip install pytube


# Global Variables
LOG = ''
CURRENT_SCRIPT_NAME = os.path.basename(__file__).split('.')[0]

# Directories
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
DOWNLOADS_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "Downloads")
LOGS_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "Logs")


# Logger
def logger():
    
    global LOG

    LOG = logging.getLogger(__name__)
    LOG.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(funcName)s : %(lineno)d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

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
    LOG.addHandler(file_handler)
    
    # StreamHandler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    LOG.addHandler(stream_handler)


# Download YouTube Video
def download_youtube_video(youtube_url):

    LOG.debug("- Download YouTube Video -")

    try:

        # YouTube Object
        LOG.debug("Create YouTube Object")
        yt = YouTube(youtube_url)

        # Select Stream
        LOG.debug("Select YouTube Stream")
        # youtube_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first()
        youtube_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        # Download YouTube Video
        LOG.debug("Download YouTube Video")
        youtube_stream.download(DOWNLOADS_DIRECTORY)

        LOG.debug("Download Completed")
    except Exception as e:
        LOG.error("Failed to download youtube video")
        LOG.error(e, exc_info=True)


# Main
if __name__ == "__main__":

    logger()

    LOG.debug("--- Start ---")

    try:
        youtube_url = input("Enter YouTube URL: ")

        # Download YouTube Video
        download_youtube_video(youtube_url)

    except Exception as e:
        LOG.error("Failed")
        LOG.error(e, exc_info=True)
    finally:
        LOG.debug("--- End ---")
