from tkinter import *
import json
from tkinter import messagebox
import random
import pyperclip
from tkinter import simpledialog
import pygame

# Global variables for UI color scheme
GREEN = "#85C61D"
DARK_ORANGE_LOGO_COLOR = "#e45231"
# set your security key here
SECURITY_KEY = "yoursecuritykey"


# ------------------------------------------------ FIND FUNCTION------------------------------------------------------ #

# once search button is clicked searches through data.json & retrieves relevant App login details if security key is valid
def find_login_details():
    # a pop-up will appear to enter security key, user can select yes to proceed or no to cancel
    yes_or_no = messagebox.askquestion(title="Security", message="please enter security key")
    # if yes is selected proceed, if no cancels process and returns to home-screen
    if yes_or_no == "yes":
        # prompts for security key
        security_key_check = simpledialog.askstring("Security", "Please enter security key.")
        # if user does not cancel proceed, else cancel process
        if security_key_check is not None:
            # if user input matches set security key proceed, else displays incorrect key try again pop-up message calls find_password() again!
            if security_key_check == SECURITY_KEY:
                # display success message, uses data input from user to search for relevant app login details
                messagebox.showinfo(title="Success", message="security check successful!")
                searched_for = app_input.get()
                # searches for data.json if not found display error message! else it retrieves login details and displays it.
                try:
                    with open("data.json") as data_file:
                        data = json.load(data_file)
                except FileNotFoundError:
                    messagebox.showinfo(title="error", message="No Data File Found.")
                else:
                    if searched_for in data:
                        retrieved_email = data[searched_for]["email"]
                        retrieved_password = data[searched_for]["password"]
                        messagebox.showinfo(title="Your Details", message=f"{searched_for}\n{retrieved_email}\n{retrieved_password}")
                    else:
                        # if app name and login details have not been logged displays error message does not exist in data!
                        messagebox.showinfo(title="Error", message=f" the following: '{app_input.get()}' does not exist in database.")
            else:
                messagebox.askquestion(title="Security Error", message="Incorrect try again.")
                find_login_details()
        else:
            pass
    else:
        pass


# ---------------------------------------------- SOUNDS FUNCTIONS --------------------------------------------------- #

# initializes, loads music file & plays music that fades in slowly + play continuously loops song
pygame.mixer.init()
pygame.mixer.music.load("music/music.wav")
pygame.mixer.music.play(loops=-1, fade_ms=100000)


# plays song that fade's in and displays img to switch sound off, also alters the command output for sound to switch off
def sound_on():
    pygame.mixer.music.play(loops=-1, fade_ms=100000)
    photo_sound_off.config(file="imgs/sound_off.png")
    sound_off_toggle.config(command=sound_off)


# switches sound off, renders sound on img, also alters the command output for sound to switch on
def sound_off():
    pygame.mixer.music.stop()
    photo_sound_off.config(file="imgs/Sound_on.png")
    sound_off_toggle.config(command=sound_on)


# ---------------------------------------------- PASSWORD GENERATOR ------------------------------------------------- #


def generate_password():

    # lists to choose characters from
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # random characters between certain ranges are chosen from list above
    password_letters = [random.choice(letters) for x in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for x in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for x in range(random.randint(2, 4))]

    # random characters added together into a list and shuffles the list order
    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    # joins the characters from list together and returns a string
    password2 = "".join(password_list)

    # inputs new generated password into the password field in UI & if deletes previous data in the field
    password_input.delete(0, END)
    password_input.insert(0, password2)

    # copies password to clip board
    pyperclip.copy(password2)


# ------------------------------------- SAVE PASSWORD FUNCTIONALITY ----------------------------------------------- #


def save():
    # retrieves user input data from app, email & password fields
    app = app_input.get()
    email = email_or_username_input.get()
    password = password_input.get()

    # json format for data being saved
    new_data = {
        app: {
            "email": email,
            "password": password,
        }
    }

    # checks validity of the data in app & password (fields cannot be empty) through a condition
    if len(app) == 0 or len(password) == 0:

        # displays error popup message box if data is invalid
        messagebox.showinfo(title="INVALID ENTRY!", message="please fill out all fields! example: \nWebsite:facebook \nEmail/username: someone@mail.com \nPassword: Pass1word2is3ok4")

    # if data is valid proceeds to try open data file where all confidential info is stored
    else:
        # try to open file and read data
        try:
            with open("data.json", "r") as data_file:
                # reading old data from data.json
                data = json.load(data_file)
        # if failed, 404 error create new file and add new data from user input
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        # updates/adds new data in data.json file if no errors occur
        else:
            # updating data.json file
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # saving updated data to data.json
                json.dump(data, data_file, indent=4)

        # clears data in input fields
        finally:
            app_input.delete(0, END)
            password_input.delete(0, END)


# -------------------------------------------------- UI SETUP -------------------------------------------------------- #

# UI setup, styling, size, logo, and grid system.
window = Tk()
window.title("Password Manager",)
window.config(bg="black", padx=30, pady=20)
window.minsize(width=600, height=400)
window.iconbitmap("imgs/logo.ico")
canvas = Canvas(width=200, height=200, bg="black", highlightthickness=0)
logo = PhotoImage(file='imgs/logo.png')
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

photo_sound_off = PhotoImage(file="imgs/sound_off.png")
sound_off_canvas = Canvas(width=20, height=20, highlightthickness=0)
sound_off_canvas.create_image(20, 20, image=photo_sound_off)
sound_off_canvas.grid(column=2, row=0, sticky=NE)

# labels
website_label = Label(text="App:", font=("arial", 15, "normal"), anchor="e", justify="right", bg="black", fg=DARK_ORANGE_LOGO_COLOR)
email_or_username_label = Label(text="Email/Username:", font=("arial", 15, "normal"), bg="black", fg=DARK_ORANGE_LOGO_COLOR)
password = Label(text="Password:", font=("arial", 15, "normal"), bg="black", fg=DARK_ORANGE_LOGO_COLOR)
# labels grid position
website_label.grid(column=0, row=1, sticky=E)
email_or_username_label.grid(column=0, row=2, sticky=E)
password.grid(column=0, row=3, sticky=E)

# Entry fields
app_input =  Entry(width=44)
app_input.focus()
email_or_username_input = Entry(width=53)
# Populates field with your email, so you don't have to type it out everytime.
email_or_username_input.insert(0, "youremail@gmail.com")
password_input = Entry(width=32)
# Entry's positions placement
app_input.grid(column=1, row=1, columnspan=2, pady=3, sticky=W)
email_or_username_input.grid(column=1, row=2, columnspan=2, pady=3)
password_input.grid(column=1, row=3, pady=3, stick=W)

# Button's & functions/commands to execute when pressed
search_button = Button(text="Search", command=find_login_details, font=("Arial", 8, "bold"), width=6, height=-1, bg=GREEN, fg="black", bd=0)
sound_off_toggle = Button(text="sounds off", image=photo_sound_off, command=sound_off, bd=0, bg="black", width=30, height=30)
generate_password_button = Button(text="Generate Password", font=("Arial", 8, "bold"), command=generate_password, bd=0, width=16, bg=GREEN, fg="black")
save_button = Button(text="Save", font=("Arial", 8, "bold"), command=save, width=45, bg=GREEN, fg="black", bd=0)
# Button's position
search_button.grid(column=1, row=1, columnspan=2, sticky=E)
sound_off_toggle.grid(column=2, row=0, sticky=NE)
generate_password_button.grid(column=1, row=3, columnspan=2, sticky=E, pady=3)
save_button.grid(column=1, row=4, columnspan=2, pady=3)


window.mainloop()
