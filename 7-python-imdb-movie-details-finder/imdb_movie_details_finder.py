import os
import sys
import logging
import datetime
from tkinter import *
from io import BytesIO
from datetime import timedelta
import requests # pip install requests
from imdb import Cinemagoer # pip install cinemagoer
from PIL import Image, ImageTk # pip install pillow

# - Global Variables - #
log = ""
cinemagoer_obj = Cinemagoer()

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
    log.addHandler(file_handler)
    
    '''
    # StreamHandler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    # '''


# Display Welcome Message
def display_welcome_msg():
    # log.debug("- Display Welcome Message -")

    print("# ----- IMDB Movie Details Finder ----- #")


# Enter Seaarch Term
def enter_search_term():
    # log.debug("- Enter Search Term -")

    search_term = input("\nSearch Movie: ")

    return search_term


# Check Search Results
def check_search_results(search_results, search_term):

    try:
        num_results = len(search_results)

        log.debug(num_results)

        no_results = True

        while(1):

            for i in range(num_results):
                values = search_results[i].values()
                if 'movie' in values:
                    no_results = False
                    break

            if no_results:
                user_decision = ""

                print(f"\nNo results found for '{search_term}'")

                print("\nWhat would you like to do?")
                print("1. Try again")
                print("2. Exit")

                user_decision = int(input("\nSelect Option: "))

                if user_decision == 1:
                    search_term = enter_search_term()
                    search_results = cinemagoer_obj.search_movie(search_term)
                    num_results = len(search_results)
                    continue
                elif user_decision == 2:
                    print("\n- Exit -")
                    sys.exit(0)
                else:
                    print("\nWrong choice. Please select a different value.")
            else:
                return search_results
    except Exception as e:
        log.error(e)


# Search Movie Term
def search_movie_term(search_term):

    try:
        search_results = cinemagoer_obj.search_movie(search_term)


        # Check Search Results
        search_results = check_search_results(search_results, search_term)

        # log.debug(search_results)

        num_results = len(search_results)

        # Filter out only 'movies' from search results
        filtered_search_results = []

        for i in range(num_results):
            values = search_results[i].values()
            
            if 'movie' in values:
                movie_name = search_results[i].values()[-2]
                movie_poster_url = search_results[i].values()[-1]

                log.debug(movie_poster_url)

                filtered_search_result = {}
                if '(None)' not in movie_name and '(None)' not in movie_poster_url:
                    movie_id = search_results[i].getID()
                    filtered_search_result['movie_id'] = movie_id
                    filtered_search_result['movie_name'] = movie_name
                    filtered_search_result['movie_poster_url'] = movie_poster_url

                    # log.debug(movie_name)

                    if '(' in movie_name and ')' in movie_name:
                        filtered_search_results.append(filtered_search_result.copy())
        
        # log.debug(filtered_search_results)
        
        # Sort Search Results by Year
        sorted_movies_list = sorted(filtered_search_results, key = lambda i: i['movie_name'].split(" ")[-1].split('(')[1].split(')')[0])

        log.debug("sorted_movies_list")
        log.debug(sorted_movies_list)

        return sorted_movies_list
    except Exception as e:
        log.error("Failed to search movie")
        log.error(e)


# Display Search Results
def display_search_results(search_results):
    
    num_search_results = len(search_results)

    print(f"\n# - {num_search_results} Results Found - #")
    for i in range(num_search_results):
        print(f"{i+1}. {search_results[i]['movie_name']}")


# Get Movie Details
def get_movie_details(id):
    return cinemagoer_obj.get_movie(id)


# Display Movie Details
def display_movie_details(movie_details):
    try:
        movie_info = {}

        print()
        movie_info['Title'] = movie_details['title']
        movie_info['Year'] = movie_details['year']
        movie_info['Original Air Date'] = movie_details['original air date']
        movie_info['Runtime'] = str(timedelta(minutes=int(movie_details['runtimes'][0]))) if movie_details.get('runtimes', 'N/A') != 'N/A' else 'N/A'
        movie_info['MPAA Rating'] = movie_details.get('certificates', 'N/A')
        movie_info['Rating'] = movie_details.get('rating', 'N/A')
        movie_info['Genres'] = movie_details['genres']
        movie_info['Aspect Ratio'] = movie_details.get('aspect ratio', 'N/A')
        movie_info['Director'] = movie_details['director'][0].values()[0] if movie_details.get('director', 'N/A') != 'N/A' else 'N/A'
        movie_info['Composer'] = movie_details['composer'][0].values()[0] if movie_details.get('composer', 'N/A') != 'N/A' else 'N/A'
        movie_info['Plot Outline'] = movie_details['plot outline'] if movie_details.get('plot outline', 'N/A') != 'N/A' else movie_details.get('plot', 'N/A')[0]

        # Print Details
        print("--- Selected Movie Details ---\n")
        for key, value in movie_info.items():
            print(f"{key}: {value}\n")
    except Exception as e:
        log.error("Failed to display movie details")
        log.error(e, exc_info=True)


# Display Movie Poster
def display_movie_poster(movie_poster_url, movie_name):

    print("Diplay Movie Poster?")
    print("1. Yes")
    print("2. No")

    display_poster_option = int(input("\nChoice: "))

    while(1):
        if display_poster_option == 1:
            print("\nDiplay Movie Poster")
            movie_poster_url_response = requests.get(movie_poster_url)

            img = Image.open(BytesIO(movie_poster_url_response.content))

            movie_poster_width = 450

            width_percent = (movie_poster_width/float(img.size[0]))
            movie_poster_height = int((float(img.size[1])*float(width_percent)))

            img_resized = img.resize((movie_poster_width, movie_poster_height), Image.ANTIALIAS)
            
            # Tkinter Window
            root = Tk()

            tk_img = ImageTk.PhotoImage(img_resized)
            
            root.title(f"{movie_name} Movie Poster")
            img_label = Label(root, image=tk_img, bd=2)
            img_label.grid(row = 10, column = 0, padx = 1, pady = 1)
            root.mainloop()

            break
        elif display_poster_option == 2:
            print("Movie Poster Not Displayed")
            break
        else:
            print("\nWrong choice selected. Please Try Again.\n")

            print("Diplay Movie Poster?")
            print("1. Yes")
            print("2. No")

            display_poster_option = int(input("\nChoice: "))


# Main
if __name__ == "__main__":

    logger()

    log.debug("# ----- Start ----- #")

    try:
        # Display Welcome Message
        display_welcome_msg()

        # Ask to enter a search term
        search_term = enter_search_term()

        # Search Movie Term
        search_results = search_movie_term(search_term)

        # Display Search Results
        display_search_results(search_results)

        # Choose movie
        choice = int(input("\nChoose Movie: "))

        while(1):
            if choice < 0 or choice > len(search_results):
                print("\nWrong choice. Please try again.")
                # Display Search Results
                display_search_results(search_results)

                # Choose movie
                choice = int(input("\nChoose Movie: "))
            else:
                # Extract Details of Selected Movie
                selected_movie_id = search_results[choice-1]['movie_id']
                selected_movie_name = search_results[choice-1]['movie_name']
                selected_movie_poster_url = search_results[choice-1]['movie_poster_url']
                break
        
        # Get Movie Details
        movie_details = get_movie_details(selected_movie_id)

        # Display Movie Details
        display_movie_details(movie_details)
        
        # Display Poster
        display_movie_poster(selected_movie_poster_url, selected_movie_name)
       
        # Exit
        print("\n- Exit -\n")

    except Exception as e:
        log.error("Failed to get movie details")
        log.error(e, exc_info=True)
    finally:
        log.debug("# ----- End ----- #")
