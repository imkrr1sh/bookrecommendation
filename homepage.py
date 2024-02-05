import tkinter as tk
from tkinter import ttk

def open_home_page(user_id):
    home_window = tk.Toplevel()  # Use Toplevel instead of Tk
    home_window.title("Home Page")
    
    # Create a notebook (tabbed widget)
    notebook = ttk.Notebook(home_window)
    
    # Page 1: Profile
    profile_frame = tk.Frame(notebook)
    tk.Label(profile_frame, text=f"Welcome to the project, {user_name}! This is your Profile page.").pack()
    notebook.add(profile_frame, text='Profile')
    
    # Page 2: My Books
    my_books_frame = tk.Frame(notebook)
    tk.Label(my_books_frame, text="This is your My Books page.").pack()
    notebook.add(my_books_frame, text='My Books')
    
    # Page 3: Logout
    logout_frame = tk.Frame(notebook)
    tk.Label(logout_frame, text="You are now logged out.").pack()
    notebook.add(logout_frame, text='Logout')
    
    # Pack the notebook
    notebook.pack(expand=True, fill='both')

# Test the function
if __name__ == "__main__":
    open_home_page("John")
