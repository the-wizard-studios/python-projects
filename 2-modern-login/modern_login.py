# Import Libraries
import os
import sys
import logging
import datetime

# Tkinter
from tkinter import *
from tkinter import messagebox

# CustomTkinter
import customtkinter # pip install customtkinter
customtkinter.set_appearance_mode("dark")

# Resolution
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

# Image Library
from PIL import Image, ImageTk # pip install Pillow

# - Global Variables - #
LOG = ""

# Tkinter Varibles
ROOT = customtkinter.CTk()
TKINTER_WIDGETS = {}
APP_WIDTH = 350
APP_HEIGHT = 320

# Current Script Name
CURRENT_SCRIPT_NAME = os.path.basename(__file__).split('.')[0]

# Directories
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "Config")
IMAGES_DIRECTORY = os.path.join(CONFIG_DIRECTORY, "Images")
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


# Homepage
def homepage():
    LOG.debug("- Homepage -")

    global ROOT
    global TKINTER_WIDGETS

    try:
        # Read the Image
        img = Image.open(os.path.join(IMAGES_DIRECTORY, "python-logo.png"))
        img_resized = img.resize((100, 100))
        img = ImageTk.PhotoImage(img_resized)

        # Label Image
        TKINTER_WIDGETS['label_img'] =  customtkinter.CTkLabel(master=ROOT, image=img, corner_radius=7)
        TKINTER_WIDGETS['label_img'].image = img
        TKINTER_WIDGETS['label_img'].grid(row=0, column=0, columnspan=2, padx=15, pady=10)

        # - Frame Login - #
        frame_login = customtkinter.CTkFrame(master=ROOT, corner_radius=10)
        frame_login.grid(row=1, column=0, padx=15, pady=20)

        # Label Username
        TKINTER_WIDGETS['label_username'] =  customtkinter.CTkLabel(master=frame_login, text="Username: ", width=30, height=25, corner_radius=7)
        TKINTER_WIDGETS['label_username'].grid(row=0, column=0, padx=10, pady=20)

        # Entry Username
        TKINTER_WIDGETS['entry_username'] = customtkinter.CTkEntry(master=frame_login, placeholder_text="Enter Username", width=200, height=30, border_width=2, corner_radius=10)
        TKINTER_WIDGETS['entry_username'].grid(row=0, column=1, padx=10, columnspan=2)

        # Label Password
        TKINTER_WIDGETS['entry_password'] = customtkinter.CTkLabel(master=frame_login, text="Password: ", width=30, height=25, corner_radius=7)
        TKINTER_WIDGETS['entry_password'].grid(row=1, column=0, padx=10, pady=5, sticky='e')

        # Entry Password
        TKINTER_WIDGETS['entry_password'] = customtkinter.CTkEntry(master=frame_login, placeholder_text="Enter Password", width=200, height=30, border_width=2, corner_radius=10, show="•", text_font=('Roboto-Medium', 10))
        TKINTER_WIDGETS['entry_password'].grid(row=1, column=1, padx=10, columnspan=2, pady=20)

        # Button Login
        TKINTER_WIDGETS['button_login'] = customtkinter.CTkButton(master=ROOT, text="Login", width=70, fg_color="#36719F", hover_color="#3B8ED0", text_color="#FFF")
        TKINTER_WIDGETS['button_login'].grid(row=2, column=0, padx=100, sticky='e')

        # Button Cancel
        TKINTER_WIDGETS['button_cancel'] = customtkinter.CTkButton(master=ROOT, text="Cancel", fg_color="gray74", hover_color="#EEE", text_color="#000", width=70, command=exit_bot)
        TKINTER_WIDGETS['button_cancel'].grid(row=2, column=0, padx=20, sticky='e')
        
    except Exception as e:
        LOG.error("Failed")
        LOG.error(e, exc_info=True)


# Load UI
def load_ui():

    LOG.debug("- Load UI -")

    global ROOT

    # Properties
    ROOT.title("TWS - Modern Login")

    # Homepage
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
