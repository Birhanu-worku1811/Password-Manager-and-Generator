import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="OOps", message="Please fill in all the fields")

    else:
        is_okay = messagebox.askokcancel(title=website,
                                         message=f"These are the details: \nEmail: {email}\nPassword: {password}\n "
                                                 f"SAVE?? ")
        if is_okay:
            try:
                with open("data.json", "r") as data_file:
                    # reading old data
                    data = json.load(data_file)
                    # updating old data with new data
                    data.update(new_data)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    # saving updated data
                    json.dump(new_data, data_file, indent=4)
            else:
                # saving updated data
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    # saving updated data
                    json.dump(data, data_file, indent=4)

                    password_entry.delete(0, END)
                    email_entry.delete(0, END)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                email_entry.delete(0, END)
                website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #
def find_password():
    global password_label
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")

    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            result_window = Toplevel(window)
            result_window.title(website)
            result_window.config(padx=20, pady=20)

            email_or_username_label = Label(result_window, text=f"Email: {email}")
            email_or_username_label.grid(row=0, column=0, pady=5)
            email_copy_button = Button(result_window, text="Copy Email", command=lambda: pyperclip.copy(email))
            email_copy_button.grid(row=0, column=1, padx=5)

            password_label = Label(result_window, text=f"Password: {password}")
            password_label.grid(row=1, column=0, pady=5)
            password_copy_button = Button(result_window, text="Copy Password", command=lambda: pyperclip.copy(password))
            password_copy_button.grid(row=1, column=1, padx=5)

        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists")
# ---------------------------- Find Password------------------------------- #


window = Tk()
window.title("My Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
account_label = Label(text="Email/Username:")
account_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "birhanuworku2011@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=2)
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
