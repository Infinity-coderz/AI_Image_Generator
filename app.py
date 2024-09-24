import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import re
import requests
from PIL import Image, ImageTk
from io import BytesIO
from bs4 import BeautifulSoup

# Initialize the app
app = ctk.CTk()  # Create the main window (app)
app.geometry("1000x720")  # Set window size
app.title("AI Image Generator")  # Set title
app.config(bg="#333")  # Set background color to black

# Function to download images
def download_image(image_data, image_counter):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        image_data.save(file_path)
        print(f"Image {image_counter} saved as {file_path}")

# Function to generate and download images
def img_gen(user_input, num_images=4):  # Use user_input as a prompt for generating images
    try:
        user = user_input  # Assign the input from entry to the user variable

        # URL for Bing image search query
        search_url = f"https://www.bing.com/images/search?q={user.replace(' ', '+')}"

        # Send a request to the search page
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(search_url, headers=headers)

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all image containers
        image_elements = soup.find_all("a", {"class": "iusc"})

        # Initialize the image counter
        image_counter = 1

        # Clear existing images and widgets from below the button
        for widget in image_frame.winfo_children():
            widget.destroy()

        # Loop through image elements and extract the URLs
        for image in image_elements:
            if image_counter > num_images:  # Stop when the specified number of images is reached
                break

            # Extract the image URL using regex
            m = re.search(r"murl\":\"(.*?)\"", str(image))
            if m:
                image_url = m.group(1)
                print(f"Downloading image: {image_url}")
                try:
                    # Fetch the image
                    img_response = requests.get(image_url)

                    # Open the image
                    img = Image.open(BytesIO(img_response.content))
                    img.save(f"Images/image_{image_counter}.png")

                    # Resize image for display
                    img_resized = img.resize((150, 150))  # Ensure images are resized to a fixed size
                    img_tk = ImageTk.PhotoImage(img_resized)

                    # Create a frame for each image and download button
                    image_container = ctk.CTkFrame(image_frame, width=180, height=220)  # Set a fixed size for the frame
                    image_container.grid(row=(image_counter - 1) // 2, column=(image_counter - 1) % 2, padx=20, pady=20)

                    # Create a label for the image
                    image_label = ctk.CTkLabel(image_container, image=img_tk, text="")
                    image_label.image = img_tk  # Keep a reference to avoid garbage collection
                    image_label.pack(pady=5)

                    # Create a download button for the image
                    download_button = ctk.CTkButton(image_container, text="Download",
                                                    command=lambda img=img, cnt=image_counter: download_image(img, cnt))
                    download_button.pack(pady=5)

                    # Increment the counter after showing the image
                    image_counter += 1

                except Exception as e:
                    print(f"Could not process image {image_url}: {e}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Function for button action
def on_button_click():
    user_input = entry.get()  # Get the input from the entry widget
    print(f"User input: {user_input}")
    img_gen(user_input)  # Call the img_gen function with the user input


# Create a label for instructions (optional)
label = ctk.CTkLabel(app, text="AI Image Generator", text_color="white", bg_color="#333", font=("Poppins", 40))
label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)  # Center the label

# Create an input field (Entry widget)
entry = ctk.CTkEntry(app, width=300, height=40, corner_radius=10, fg_color="gray25", text_color="white", border_width=2, font=("Poppins", 15))
entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)  # Center the input field

# Create a button (with blue color)
button = ctk.CTkButton(app, text="Generate", command=on_button_click, width=200, height=40, corner_radius=20, hover_color="blue", font=("Poppins", 20))
button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)  # Center the button

# Create a frame for displaying images below the button
image_frame = ctk.CTkFrame(app, width=800, height=400)
image_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# Start the app
app.mainloop()
