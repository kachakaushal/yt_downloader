import customtkinter as ctk
import yt_dlp
import webbrowser
import re
import tkinter.messagebox
from tkinter import filedialog  # To open a file dialog for directory selection

def yt_open():
    webbrowser.open("https://www.youtube.com")
# Progress update function (to show percentage only)
def progress_hook(d):
    """Update the progress bar and percentage based on download status."""
    if d['status'] == 'downloading':
        # Extract the progress percentage
        raw_percent = d.get('_percent_str', '0.00%')
        clean_percent = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', raw_percent).strip('%')
        try:
            percent = float(clean_percent)
            percentage_label.configure(text=f"{percent:.2f}%")  # Update percentage label
        except ValueError:
            percentage_label.configure(text="0%")  # Reset percentage if invalid

def download_video():
    video_url = url_entry.get()
    quality = quality_var.get()
    download_type = download_type_var.get()

    # Use the default path if none is selected
    download_path = custom_path_var.get() or "."

    if not video_url:
        tkinter.messagebox.showerror("Error", "Please enter a valid YouTube URL!")  # Use tkinter's messagebox
        return

    # Determine the format options
    if download_type == "Audio Only":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{download_path}/%(title)s_audio.%(ext)s',
            'progress_hooks': [progress_hook],
            'noplaylist': True,
        }
    else:
        ydl_opts = {
            'format': f'bestvideo[height={quality}]+bestaudio/best',
            'outtmpl': f'{download_path}/%(title)s_%(resolution)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'noplaylist': True,
        }

    try:
        percentage_label.configure(text="0%")  # Reset percentage label
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        tkinter.messagebox.showinfo("Success", "Download completed successfully!")  # Use tkinter's messagebox
    except Exception as e:
        tkinter.messagebox.showerror("Error", f"An error occurred: {e}")  # Use tkinter's messagebox

# Function to open the directory picker dialog
def choose_download_directory():
    selected_directory = filedialog.askdirectory()  # Open directory dialog
    if selected_directory:
        custom_path_var.set(selected_directory)  # Set the chosen path

# Configure customtkinter appearance
ctk.set_appearance_mode("Light")  # Light mode for the UI
ctk.set_default_color_theme("green")  # Green color theme

# Create the main application window
root = ctk.CTk()
root.title("YouTube Downloader")
root.geometry("700x700")

#youtube button
youtube_button = ctk.CTkButton(root, text="youtube", command=yt_open, corner_radius=8, fg_color="green", hover_color="dark green")
youtube_button.pack(pady=20)
# URL input
url_label = ctk.CTkLabel(root, text="YouTube Video URL:", font=("Arial", 14))
url_label.pack(pady=10)
url_entry = ctk.CTkEntry(root, width=400, placeholder_text="Enter YouTube URL")
url_entry.pack(pady=5)

# Quality options
quality_label = ctk.CTkLabel(root, text="Select Quality:", font=("Arial", 14))
quality_label.pack(pady=10)
quality_var = ctk.StringVar(value="720")  # Default value
qualities = [("144p", "144"), ("240p", "240"), ("360p", "360"),
             ("480p", "480"), ("720p", "720"), ("1080p", "1080")]

quality_frame = ctk.CTkFrame(root)
quality_frame.pack(pady=5)
for text, value in qualities:
    ctk.CTkRadioButton(quality_frame, text=text, variable=quality_var, value=value).pack(side="left", padx=5)

# Download type
download_type_label = ctk.CTkLabel(root, text="Download Type:", font=("Arial", 14))
download_type_label.pack(pady=10)
download_type_var = ctk.StringVar(value="Video + Audio")
ctk.CTkRadioButton(root, text="Video + Audio", variable=download_type_var, value="Video + Audio").pack()
ctk.CTkRadioButton(root, text="Audio Only", variable=download_type_var, value="Audio Only").pack()

# Custom download path
download_path_label = ctk.CTkLabel(root, text="Custom Download Path:", font=("Arial", 14))
download_path_label.pack(pady=10)
custom_path_var = ctk.StringVar()  # To store the custom path
path_entry = ctk.CTkEntry(root, textvariable=custom_path_var, width=400, placeholder_text="Choose download path")
path_entry.pack(pady=5)

# Button to open the file dialog for custom path
choose_path_button = ctk.CTkButton(root, text="Choose Path", command=choose_download_directory)
choose_path_button.pack(pady=10)

# Percentage display
percentage_label = ctk.CTkLabel(root, text="0%", font=("Arial", 18), text_color="blue")
percentage_label.pack(pady=20)

# Download button
download_button = ctk.CTkButton(root, text="Download", command=download_video, corner_radius=8, fg_color="green", hover_color="dark green")
download_button.pack(pady=20)

# Run the application
root.mainloop()