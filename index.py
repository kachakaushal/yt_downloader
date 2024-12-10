import tkinter as tk
from tkinter import messagebox

# Sample credentials
USER_CREDENTIALS = {"username": "admin", "password": "password123"}

# Function to check login
def authenticate():
    username = entry_username.get()
    password = entry_password.get()
    
    # Check if the entered credentials match the predefined ones
    if username == USER_CREDENTIALS["username"] and password == USER_CREDENTIALS["password"]:
        messagebox.showinfo("Success", "Login successful!")
        open_main_window()  # Open another window upon successful login
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Function to open the main window after successful login
def open_main_window():
    # Close the login window
    login_window.destroy()
    
    # Create a new window (this could be your main application window)
    main_window = tk.Tk()
    main_window.title("Main Application")
    
    label = tk.Label(main_window, text="Welcome to the application!", font=("Arial", 20))
    label.pack(pady=20)
    
    main_window.geometry("400x200")
    main_window.mainloop()

# Create the login window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("400x300")

# Create and pack the username label and entry
label_username = tk.Label(login_window, text="Username:")
label_username.pack(pady=10)
entry_username = tk.Entry(login_window)
entry_username.pack(pady=10)

# Create and pack the password label and entry
label_password = tk.Label(login_window, text="Password:")
label_password.pack(pady=10)
entry_password = tk.Entry(login_window, show="*")
entry_password.pack(pady=10)

# Create and pack the login button
login_button = tk.Button(login_window, text="Login", command=authenticate)
login_button.pack(pady=20)

# Run the Tkinter main loop
login_window.mainloop()
