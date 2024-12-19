import customtkinter as ctk
import mysql.connector
import smtplib
import random
import string
import time
from tkinter import messagebox

# Function to connect to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",       # Your host
        user="root",            # Your MySQL username
        password="",    # Your MySQL password
        database="login_user"    # Your database name
    )

# Function to generate a random OTP
def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))  # Generate a 6-digit OTP
    return otp

# Function to send OTP to user's email
def send_otp_email(to_email, otp):
    try:
        sender_email = "your_email@gmail.com"  # Replace with your Gmail email
        sender_password = "your_password"  # Replace with your Gmail password
        subject = "Your OTP Code"
        body = f"Your OTP code is {otp}. It will expire in 5 minutes."

        # Create the email content
        message = f"Subject: {subject}\n\n{body}"

        # Set up the Gmail SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message)
            print("OTP sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to handle login authentication with OTP
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
    query = "SELECT email FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        # Generate OTP and send it to the user's email
        email = user[0]
        otp = generate_otp()
        send_otp_email(email, otp)

        # Store the OTP and its expiration time (5 minutes)
        otp_expiry_time = time.time() + 300  # OTP expires in 5 minutes
        otp_data[username] = {"otp": otp, "expiry": otp_expiry_time}

        # Ask user to input OTP for verification
        otp_window(username)
    else:
        messagebox.showerror("Error", "Invalid credentials")

    cursor.close()
    conn.close()

# Dictionary to store OTP and expiry time for each user
otp_data = {}

# Function to create OTP input window
def otp_window(username):
    otp_window = ctk.CTkToplevel(app)
    otp_window.title("Enter OTP")
    otp_window.geometry("300x200")

    label_otp = ctk.CTkLabel(otp_window, text="Enter OTP:")
    label_otp.pack(pady=10)

    entry_otp = ctk.CTkEntry(otp_window)
    entry_otp.pack(pady=10)

    def verify_otp():
        entered_otp = entry_otp.get()
        if username in otp_data:
            otp_info = otp_data[username]
            if time.time() < otp_info["expiry"]:
                if entered_otp == otp_info["otp"]:
                    messagebox.showinfo("Success", "Login Successful")
                    otp_window.destroy()
                else:
                    messagebox.showerror("Error", "Invalid OTP")
            else:
                messagebox.showerror("Error", "OTP expired")
                otp_window.destroy()
        else:
            messagebox.showerror("Error", "OTP not found")

    otp_button = ctk.CTkButton(otp_window, text="Verify OTP", command=verify_otp)
    otp_button.pack(pady=20)

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
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, password))
        conn.commit()
        messagebox.showinfo("Success", "User Registered Successfully")
        clear_signup_fields()
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username or Email already exists")

    cursor.close()
    conn.close()

# Function to clear signup fields
def clear_signup_fields():
    entry_signup_username.delete(0, ctk.END)
    entry_signup_email.delete(0, ctk.END)
    entry_signup_password.delete(0, ctk.END)

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

# Start with the login screen
signup_frame.pack_forget()

# Run the application
app.mainloop()
