import os
import sys
import logging
import datetime

# import requests
from pytube import YouTube

# Tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

# CustomTkinter
import customtkinter
customtkinter.set_appearance_mode("dark")

# Resolution
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

# Image Library
from PIL import Image, ImageTk


# - Global Variables - #
LOG = ""
# Tkinter Varibles
ROOT = customtkinter.CTk()
TKINTER_WIDGETS = {}
APP_WIDTH = 570
APP_HEIGHT = 320

# Current Script Name
CURRENT_SCRIPT_NAME = os.path.basename(__file__).split('.')[0]

# Directories
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "Config")
IMAGES_DIRECTORY = os.path.join(CONFIG_DIRECTORY, "Images")
LOGS_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "Logs")

# Downloads Folder
DOWNLOADS_FOLDER = os.path.join(f'C:{os.sep}', 'Users', os.environ['username'], 'Downloads')


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


# Quit Homepage
def quit_homepage():
    LOG.debug("- Quit Homepage -")

    global ROOT
    
    # Quit Homepage
    ROOT.destroy()


# Exit Bot
def exit_bot():
    LOG.debug("- Exit Bot -")

    # Quit Homepage
    quit_homepage()

    # Exit
    LOG.debug("Exit Bot")
    sys.exit(0)


# Change Download Path
def change_download_path():
    global DOWNLOADS_FOLDER
    global TKINTER_WIDGETS

    LOG.debug("- Change Download Path -")

    try:
        new_downloads_folder = filedialog.askdirectory()

        if len(new_downloads_folder) != 0:
            DOWNLOADS_FOLDER = new_downloads_folder
        
        TKINTER_WIDGETS['entry_download_path'].delete(0, END)
        TKINTER_WIDGETS['entry_download_path'].insert(0, DOWNLOADS_FOLDER)

    except Exception as e:
        LOG.error("Failed to change donwload path")
        LOG.error(e, exc_info=True)


# Download Video
def download_video():
    global TKINTER_WIDGETS

    LOG.debug("- Download Video -")

    try:
        youtube_obj = YouTube(TKINTER_WIDGETS['entry_youtube_url'].get())

        # quit_homepage()

        # Disable buttons
        TKINTER_WIDGETS['button_download'].configure(state=DISABLED)

        # Low Quality
        youtube_video = youtube_obj.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first()

        # High Quality
        # youtube_video = youtube_obj.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        youtube_obj.register_on_complete_callback(notify_download_completed)

        youtube_video.download(DOWNLOADS_FOLDER)

    except Exception as e:
        LOG.error("Failed to Download Video")
        LOG.error(e, exc_info=True)


# Notify Download Completed
def notify_download_completed(stream, file_handle):
    global TKINTER_WIDGETS

    LOG.debug("- Notify Download Completed -")
    
    TKINTER_WIDGETS['button_download'].configure(state=NORMAL)

    window = Tk()
    window.eval(f'tk::PlaceWindow {window.winfo_toplevel()}')
    window.iconify()

    # Icon
    window.iconbitmap(os.path.join(IMAGES_DIRECTORY, 'youtube.ico'))

    # Title
    # window.title("YouTube")

    # Message Box
    messagebox.showinfo("Youtube Downloader", "Download Completed!")
    
    # Quit Window
    window.deiconify()
    window.destroy()
    window.quit()


# Homepage
def homepage():

    global ROOT
    global TKINTER_WIDGETS

    try:
         # Read the Image
        img = Image.open(os.path.join(IMAGES_DIRECTORY, "youtube.png"))
        img_resized = img.resize((450, 100))
        img = ImageTk.PhotoImage(img_resized)

        TKINTER_WIDGETS['label_img'] =  customtkinter.CTkLabel(master=ROOT, image=img, corner_radius=7)
        TKINTER_WIDGETS['label_img'].image = img
        TKINTER_WIDGETS['label_img'].grid(row=0, column=0, columnspan=3, padx=15, pady=10)

        # - Frame YouTube - #
        frame_yt = customtkinter.CTkFrame(master=ROOT, corner_radius=10)
        frame_yt.grid(row=1, column=0, padx=15, pady=20, columnspan=3)

        # Label YouTube URL
        TKINTER_WIDGETS['label_youtube_url'] =  customtkinter.CTkLabel(master=frame_yt, text="YouTube URL: ", width=30, height=25, corner_radius=7)
        TKINTER_WIDGETS['label_youtube_url'].grid(row=0, column=0, padx=10, pady=20)

        # Entry YouTube URL
        TKINTER_WIDGETS['entry_youtube_url'] = customtkinter.CTkEntry(master=frame_yt, placeholder_text="Enter YouTube URL", width=390, height=30, border_width=2, corner_radius=10)
        TKINTER_WIDGETS['entry_youtube_url'].grid(row=0, column=1, padx=10, columnspan=2)

        # Label Download Path
        TKINTER_WIDGETS['entry_download_path'] = customtkinter.CTkLabel(master=frame_yt, text="Download Path: ", width=30, height=25, corner_radius=7)
        TKINTER_WIDGETS['entry_download_path'].grid(row=1, column=0, padx=10, pady=5, sticky='e')

        # Entry Download Path
        TKINTER_WIDGETS['entry_download_path'] = customtkinter.CTkEntry(master=frame_yt, placeholder_text=DOWNLOADS_FOLDER, width=300, height=30, border_width=2, corner_radius=10, text_font=('Roboto-Medium', 10))
        TKINTER_WIDGETS['entry_download_path'].grid(row=1, column=1, padx=10, columnspan=1, pady=20, sticky='w')

        # Button Change Path
        TKINTER_WIDGETS['button_change_path'] = customtkinter.CTkButton(master=frame_yt, text="Change", width=70, fg_color="#36719F", hover_color="#3B8ED0", text_color="#FFF", command=change_download_path)
        TKINTER_WIDGETS['button_change_path'].grid(row=1, column=2, padx=10)

        # Button Download
        TKINTER_WIDGETS['button_download'] = customtkinter.CTkButton(master=ROOT, text="Download", width=70, fg_color="#0D8A66", hover_color="#11B384", text_color="#FFF", command=download_video)
        TKINTER_WIDGETS['button_download'].grid(row=2, column=0, padx=100, sticky='e')

        # Button Exit
        TKINTER_WIDGETS['button_exit'] = customtkinter.CTkButton(master=ROOT, text="Exit", fg_color="gray74", hover_color="#EEE", text_color="#000", width=70, command=exit_bot)
        TKINTER_WIDGETS['button_exit'].grid(row=2, column=0, padx=20, sticky='e')

    except Exception as e:
        LOG.error("Failed")
        LOG.error(e, exc_info=True)


# Load UI
def load_ui():

    global ROOT

    # Properties
    ROOT.title("YouTube Downloader")
    ROOT.iconbitmap(os.path.join(IMAGES_DIRECTORY, 'youtube.ico'))

    homepage()

    #  - Set Window to appear in the middle when program runs -
    screen_width = ROOT.winfo_screenwidth()
    screen_height = ROOT.winfo_screenheight()

    app_center_coordinate_x = (screen_width / 3) - (APP_WIDTH / 3)
    app_center_coordinate_y = (screen_height / 3) - (APP_HEIGHT / 3)

    # Position App to the Centre of the Screen
    ROOT.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{int(app_center_coordinate_x)}+{int(app_center_coordinate_y)}")

    # Prevent User from Resizing the Window
    ROOT.resizable(width=False, height=False)

    # Close 'X' Button
    ROOT.protocol("WM_DELETE_WINDOW", exit_bot)

    # Infinite Loop
    ROOT.mainloop()


# Main
if __name__ == "__main__":

    # Logger
    logger() 

    # Load UI
    load_ui()
