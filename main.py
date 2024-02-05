import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re

# Connecting to database
print("Connecting to database...")
conn = sqlite3.connect('logindata.db')
cursor = conn.cursor()

# Create Users table with 'user_id', 'first_name', 'last_name', 'email', 'username', and 'password' columns
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    user_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT,
                    username TEXT UNIQUE,
                    password TEXT
                )''')
conn.commit()

# Read data from Books.csv and Ratings.csv files
books_df = pd.read_csv('Books.csv', encoding='latin-1')
ratings_df = pd.read_csv('Ratings.csv', encoding='latin-1')

# Merge the two dataframes on the ISBN column
merged_df = pd.merge(ratings_df, books_df, on='ISBN')

# Function to validate login credentials
def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    cursor.execute('''SELECT user_id FROM Users WHERE username = ? AND password = ?''', (username, password))
    user_id = cursor.fetchone()

    if user_id:
        login_window.destroy()  # Close login window
        open_home_page(user_id[0])  # Show home page with user ID
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to handle user signup
def signup():
    signup_window = tk.Toplevel(login_window)
    signup_window.title("Sign Up")

    def create_user():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        username = username_entry.get()
        re_enter_email = re_enter_email_entry.get()
        password = password_entry.get()
        re_enter_password = re_enter_password_entry.get()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Sign Up Failed", "Invalid email format")
            return

        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(
                char.isalnum() for char in password):
            messagebox.showerror("Sign Up Failed",
                                 "Password must be at least 8 characters long and contain at least 1 number and 1 special character")
            return

        if password != re_enter_password:
            password_mismatch_label.config(text="Passwords do not match", fg="red")
            return
        else:
            password_mismatch_label.config(text="")

        if email != re_enter_email:
            email_mismatch_label.config(text="Emails do not match", fg="red")
            return
        else:
            email_mismatch_label.config(text="")

        if not first_name or not last_name or not email or not re_enter_email or not password or not re_enter_password:
            messagebox.showerror("Sign Up Failed", "Please fill all fields")
            return

        cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
        existing_email = cursor.fetchone()
        if existing_email:
            messagebox.showerror("Sign Up Failed", "Email already exists")
            return

        cursor.execute(
            "INSERT INTO Users (first_name, last_name, email, username, password) VALUES (?, ?, ?, ?, ?)",
            (first_name, last_name, email, username, password))
        conn.commit()

        messagebox.showinfo("Sign Up Successful", "You have successfully signed up!")
        signup_window.destroy()

    tk.Label(signup_window, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
    first_name_entry = tk.Entry(signup_window)
    first_name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(signup_window, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
    last_name_entry = tk.Entry(signup_window)
    last_name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(signup_window, text="Email:").grid(row=2, column=0, padx=5, pady=5)
    email_entry = tk.Entry(signup_window)
    email_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(signup_window, text="Re-enter Email:").grid(row=3, column=0, padx=5, pady=5)
    re_enter_email_entry = tk.Entry(signup_window)
    re_enter_email_entry.grid(row=3, column=1, padx=5, pady=5)
    email_mismatch_label = tk.Label(signup_window, text="", fg="red")
    email_mismatch_label.grid(row=4, column=0, columnspan=2)

    tk.Label(signup_window, text="Username:").grid(row=5, column=0, padx=5, pady=5)
    username_entry = tk.Entry(signup_window)
    username_entry.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(signup_window, text="Password:").grid(row=6, column=0, padx=5, pady=5)
    password_entry = tk.Entry(signup_window, show="*")
    password_entry.grid(row=6, column=1, padx=5, pady=5)

    tk.Label(signup_window, text="Re-enter Password:").grid(row=7, column=0, padx=5, pady=5)
    re_enter_password_entry = tk.Entry(signup_window, show="*")
    re_enter_password_entry.grid(row=7, column=1, padx=5, pady=5)
    password_mismatch_label = tk.Label(signup_window, text="", fg="red")
    password_mismatch_label.grid(row=8, column=0, columnspan=2)

    tk.Button(signup_window, text="Create Account", command=create_user).grid(row=9, column=0, columnspan=2,
                                                                               padx=5, pady=5)


# Function to show home page after successful login or signup
def open_home_page(user_id):
    home_window = tk.Tk()  # Changed from Toplevel to Tk
    home_window.title("Home Page")

    notebook = ttk.Notebook(home_window)

    # Profile Tab
    profile_frame = tk.Frame(notebook)
    profile_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    tk.Label(profile_frame, text="Below are your profile details:").pack(anchor="w", padx=10, pady=5)

    user_details = get_user_details(user_id)
    tk.Label(profile_frame, text=f"User ID: {user_id}").pack(anchor="w", padx=10, pady=5)
    tk.Label(profile_frame, text=f"Username: {user_details['username']}").pack(anchor="w", padx=10, pady=5)
    tk.Label(profile_frame, text=f"Name: {user_details['name']}").pack(anchor="w", padx=10, pady=5)
    tk.Label(profile_frame, text=f"Email: {user_details['email']}").pack(anchor="w", padx=10, pady=5)

    notebook.add(profile_frame, text='Profile')

    # Book Recommendation Tab
    recommendation_frame = tk.Frame(notebook)
    recommendation_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    tk.Label(recommendation_frame, text="Book Recommendations").pack(anchor="w", padx=10, pady=5)

    # Slider for selecting book rating
    rating_label = tk.Label(recommendation_frame, text="Select minimum book rating:")
    rating_label.pack(anchor="w", padx=10, pady=5)
    rating_slider = tk.Scale(recommendation_frame, from_=0, to=10, orient="horizontal", resolution=1)
    rating_slider.pack(anchor="w", padx=10, pady=5)

    # Entry field for author's name
    author_label = tk.Label(recommendation_frame, text="Enter author's name:")
    author_label.pack(anchor="w", padx=10, pady=5)
    author_entry = tk.Entry(recommendation_frame)
    author_entry.pack(anchor="w", padx=10, pady=5)

    # Button to generate recommendations
    generate_button = tk.Button(recommendation_frame, text="Generate Recommendations",
                                 command=lambda: generate_recommendations(rating_slider.get(), author_entry.get()))
    generate_button.pack(anchor="w", padx=10, pady=5)

    notebook.add(recommendation_frame, text='Book Recommendations')

    # Logout Tab
    logout_frame = tk.Frame(notebook)
    tk.Button(logout_frame, text="Logout", command=lambda: logout(home_window)).pack()
    notebook.add(logout_frame, text='Logout')

    notebook.pack(expand=True, fill='both')


# Function to fetch user details
def get_user_details(user_id):
    cursor.execute('''SELECT first_name, last_name, email, username FROM Users WHERE user_id = ?''', (user_id,))
    user_details = cursor.fetchone()
    if user_details:
        return {
            'name': f"{user_details[0]} {user_details[1]}",
            'email': user_details[2],
            'username': user_details[3]
        }
    else:
        return "Unknown"


# Function to generate book recommendations
def generate_recommendations(min_rating, author):
    # Drop rows with missing values
    merged_df_cleaned = merged_df.dropna(subset=['Book-Rating', 'Author'])

    # Filter books based on minimum rating
    filtered_books = merged_df_cleaned[merged_df_cleaned['Book-Rating'] == min_rating]

    # If author name is provided, filter books by author
    if author:
        filtered_books = filtered_books[filtered_books['Author'].str.contains(author, case=False)]

    # If there are no books matching the criteria, display a message
    if filtered_books.empty:
        messagebox.showinfo("No Recommendations", f"No books found with a rating of {min_rating}.")
    else:
        # Display book recommendations to the user
        recommendation_window = tk.Toplevel()
        recommendation_window.title("Book Recommendations")

        recommendation_text = tk.Text(recommendation_window, wrap=tk.WORD, height=20, width=50)
        recommendation_text.pack(padx=10, pady=10)

        recommendation_text.insert(tk.END, "Book Recommendations:\n\n")
        for index, row in filtered_books.iterrows():
            recommendation_text.insert(tk.END, f"Title: {row['Title']}\n")
            recommendation_text.insert(tk.END, f"Author: {row['Author']}\n")
            recommendation_text.insert(tk.END, f"Rating: {row['Book-Rating']}\n")
            recommendation_text.insert(tk.END, "----------------------------------------\n")

        recommendation_text.configure(state='disabled')


# Function to logout
def logout(window):
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        window.destroy()
        login_window.deiconify()


# Create login window
login_window = tk.Tk()
login_window.title("Login")

# Username and Password Entry fields
tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(login_window)
username_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(login_window, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Login Button
tk.Button(login_window, text="Login", command=validate_login).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Sign Up Text and Button
tk.Label(login_window, text="If you are a new user, Please click the sign up button.").grid(row=3, column=0,
                                                                                             columnspan=2)
tk.Button(login_window, text="Sign Up", command=signup).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

login_window.mainloop()