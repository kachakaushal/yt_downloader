import customtkinter as ctk
import mysql.connector
from tkinter import messagebox

# Function to connect to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",       # Your host
        user="root",            # Your MySQL username
        password="",    # Your MySQL password
        database="tyyy"    # Your database name
    )

# Function to handle login authentication
def authenticate_user():
    username = entry_login_username.get()
    password = entry_login_password.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()

    # Query to check the credentials
    query = "SELECT * FROM login_user WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Success", "Login Successful")
        clear_login_fields()
    else:
        messagebox.showerror("Error", "Invalid credentials")

    cursor.close()
    conn.close()

# Function to handle user registration (signup)
def register_user():
    username = entry_signup_username.get()
    email = entry_signup_email.get()
    password = entry_signup_password.get()

    if not username or not email or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Query to insert a new user
        query = "INSERT INTO login_user (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, password))
        conn.commit()
        messagebox.showinfo("Success", "User Registered Successfully")
        clear_signup_fields()
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username or Email already exists")

    cursor.close()
    conn.close()

# Function to clear login fields
def clear_login_fields():
    entry_login_username.delete(0, ctk.END)
    entry_login_password.delete(0, ctk.END)

# Function to clear signup fields
def clear_signup_fields():
    entry_signup_username.delete(0, ctk.END)
    entry_signup_email.delete(0, ctk.END)
    entry_signup_password.delete(0, ctk.END)

# Function to switch between login and signup screens
def show_signup_screen():
    login_frame.pack_forget()
    signup_frame.pack(pady=20)

def show_login_screen():
    signup_frame.pack_forget()
    login_frame.pack(pady=20)

# Create the main window
app = ctk.CTk()
app.title("User Authentication")
app.geometry("400x400")

# Login Frame
login_frame = ctk.CTkFrame(app)
login_frame.pack(pady=20)

label_login_title = ctk.CTkLabel(login_frame, text="Login", font=("Arial", 24))
label_login_title.pack(pady=10)

label_login_username = ctk.CTkLabel(login_frame, text="Username:")
label_login_username.pack(pady=5)
entry_login_username = ctk.CTkEntry(login_frame)
entry_login_username.pack(pady=5)

label_login_password = ctk.CTkLabel(login_frame, text="Password:")
label_login_password.pack(pady=5)
entry_login_password = ctk.CTkEntry(login_frame, show="*")
entry_login_password.pack(pady=5)

login_button = ctk.CTkButton(login_frame, text="Login", command=authenticate_user)
login_button.pack(pady=10)

signup_button = ctk.CTkButton(login_frame, text="Don't have an account? Sign Up", command=show_signup_screen)
signup_button.pack(pady=5)

# Signup Frame
signup_frame = ctk.CTkFrame(app)

label_signup_title = ctk.CTkLabel(signup_frame, text="Sign Up", font=("Arial", 24))
label_signup_title.pack(pady=10)

label_signup_username = ctk.CTkLabel(signup_frame, text="Username:")
label_signup_username.pack(pady=5)
entry_signup_username = ctk.CTkEntry(signup_frame)
entry_signup_username.pack(pady=5)

label_signup_email = ctk.CTkLabel(signup_frame, text="Email:")
label_signup_email.pack(pady=5)
entry_signup_email = ctk.CTkEntry(signup_frame)
entry_signup_email.pack(pady=5)

label_signup_password = ctk.CTkLabel(signup_frame, text="Password:")
label_signup_password.pack(pady=5)
entry_signup_password = ctk.CTkEntry(signup_frame, show="*")
entry_signup_password.pack(pady=5)

signup_button = ctk.CTkButton(signup_frame, text="Sign Up", command=register_user)
signup_button.pack(pady=10)

login_button = ctk.CTkButton(signup_frame, text="Already have an account? Login", command=show_login_screen)
login_button.pack(pady=5)

# Start with the login screen
show_login_screen()

# Run the application
app.mainloop()
