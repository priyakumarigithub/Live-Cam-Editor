'''This code includes the following changes:

Added a timer_started boolean variable to keep track of whether the timer has started or not.
Added a capture_timer variable to count the number of frames elapsed since the hand was detected.
In the update_image_adjustments() function, when hands are detected, the timer is started if it hasn't already started.
Inside the timer check, capture_timer is incremented by 1 for each frame.
When capture_timer reaches 60 (assuming 60 frames per second), which corresponds to 1 second, the image is saved and the timer is reset.
Please note that the code assumes a frame rate of 60 frames per second, so you may need to adjust the value 60 in the if capture_timer >= 60 condition based on the actual frame rate of your camera.

Also, make sure to have the necessary libraries installed (cv2, numpy, tkinter, PIL, ttkbootstrap) and import the required modules (mp_hands, mp_drawing, mp_drawing_styles) before running the code.'''


import cv2
import numpy as np
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
from ttkbootstrap import Style
from mediapipe.python.solutions import hands as mp_hands
import os
import datetime

# Load the MediaPipe Hands model
hands = mp_hands.Hands()

# Variables for capturing the image after 3 seconds of hand detection
hand_detected = False
timer_started = False
capture_timer = 0

# Function to detect hands in the frame
def detect_hand(frame):
    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands in the frame
    results = hands.process(frame_rgb)

    return results

# Function to update the brightness, contrast, and saturation values based on the trackbar positions
def update_image_adjustments():
    # Read the frame from the camera
    ret, frame = cap.read()

    # Get the current trackbar positions for brightness, contrast, and saturation
    brightness = brightness_scale.get()
    contrast = contrast_scale.get()
    saturation = saturation_scale.get()

    # Check if auto enhance is enabled
    if auto_enhance_var.get() == 1:
        # Calculate the auto enhance values
        brightness, contrast, saturation = calculate_auto_enhance(frame)

        # Update the trackbar positions
        brightness_scale.set(brightness)
        contrast_scale.set(contrast)
        saturation_scale.set(saturation)

    # Convert the brightness, contrast, and saturation values from trackbar positions to actual values
    brightness = (brightness - 50) * 2
    contrast = contrast / 50.0
    saturation = saturation / 50.0

    # Apply the brightness, contrast, and saturation adjustments to the camera frame
    adjusted_frame = np.clip((frame * contrast + brightness), 0, 255).astype(np.uint8)
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2HSV)
    adjusted_frame[:, :, 1] = np.clip((adjusted_frame[:, :, 1] * saturation), 0, 255).astype(np.uint8)
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_HSV2BGR)
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2RGB)

    # Detect hand in the frame
    results = detect_hand(adjusted_frame)

    # Check if hands are detected
    if results.multi_hand_landmarks:
        if not hand_detected:
            # Start the timer
            global timer_started
            if not timer_started:
                timer_started = True
                global capture_timer
                capture_timer = 3
                print("Counter Start")

    # Convert the adjusted frame to PIL format
    image = Image.fromarray(adjusted_frame)

    # Convert the PIL image to Tkinter format
    tk_image = ImageTk.PhotoImage(image=image)

    # Update the image in the panel
    panel.config(image=tk_image)
    panel.image = tk_image  # Store a reference to avoid garbage collection

    # Check if the timer is started
    if timer_started:
        capture_timer += 1

        # Check if 3 seconds have passed
        if capture_timer >= 60:  # 60 frames = 1 second (assuming 60 fps)
            # Save the image
            save_image_hand()

            # Reset the timer
            timer_started = False
            capture_timer = 0

    # Schedule the next update
    root.after(20, update_image_adjustments)

# Function to calculate the auto enhance values based on the frame
def calculate_auto_enhance(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate the histogram using OpenCV
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    # Calculate the cumulative distribution function (CDF) of the histogram
    cdf = hist.cumsum() / hist.sum()

    # Calculate the auto enhance values
    brightness = np.argmax(cdf > 0.075) / 2 + 25
    contrast = (np.argmax(cdf > 0.75) - np.argmax(cdf > 0.07)) / 4
    saturation = np.argmax(cdf > 0.2) / 2 + 25

    return brightness, contrast, saturation

# Function to save the current image displayed in the panel
def save_image():
    # Read the frame from the camera
    ret, frame = cap.read()

    # Get the current trackbar positions for brightness, contrast, and saturation
    brightness = brightness_scale.get()
    contrast = contrast_scale.get()
    saturation = saturation_scale.get()

    # Convert the brightness, contrast, and saturation values from trackbar positions to actual values
    brightness = (brightness - 50) * 2
    contrast = contrast / 50.0
    saturation = saturation / 50.0

    # Apply the brightness, contrast, and saturation adjustments to the frame
    adjusted_frame = np.clip((frame * contrast + brightness), 0, 255).astype(np.uint8)
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2HSV)
    adjusted_frame[:, :, 1] = np.clip((adjusted_frame[:, :, 1] * saturation), 0, 255).astype(np.uint8)
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_HSV2BGR)
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2RGB)

    # Create a PIL image from the adjusted frame
    image = Image.fromarray(adjusted_frame)

    # Prompt the user to select a save location
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

    # Check if the user selected a save location
    if save_path:
        # Save the image to the selected path
        image.save(save_path)
        messagebox.showinfo("Image Saved", "The image has been saved successfully.")
    else:
        messagebox.showinfo("Save Cancelled", "Image save operation cancelled.")

import os

# Function to save the current image displayed in the panel
def save_image_hand():
    # Read the frame from the camera
    ret, frame = cap.read()

    # Get the current trackbar positions for brightness, contrast, and saturation
    brightness = brightness_scale.get()
    contrast = contrast_scale.get()
    saturation = saturation_scale.get()

    # Convert the brightness, contrast, and saturation values from trackbar positions to actual values
    brightness = (brightness - 50) * 2
    contrast = contrast / 50.0
    saturation = saturation / 50.0

    # Apply the brightness, contrast, and saturation adjustments to the frame
    adjusted_frame = np.clip((frame * contrast + brightness), 0, 255).astype(np.uint8)
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2HSV)
    adjusted_frame[:, :, 1] = np.clip((adjusted_frame[:, :, 1] * saturation), 0, 255).astype(np.uint8)
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_HSV2BGR)
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2RGB)

    # Create a PIL image from the adjusted frame
    image = Image.fromarray(adjusted_frame)

    # Generate a unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"image_{timestamp}.png"

    # Specify the save directory
    save_directory = "Live cam Hand Detection/img"  # Replace with your desired save directory

    # Create the save path
    save_path = os.path.join(save_directory, filename)

    try:
        # Save the image to the specified path
        image.save(save_path)
        messagebox.showinfo("Image Saved", "The image has been saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the image:\n{str(e)}")


# Create a VideoCapture object to read from the camera
cap = cv2.VideoCapture(0)  # 0 represents the default camera

# Create a Tkinter window
root = tk.Tk()
root.title("Camera and Histogram")
root.resizable(width=False, height=False)
root.configure(background='')

# Create a Frame to hold the capture panel and save button
capture_frame = tk.Frame(root,width=100, height=100)
capture_frame.pack(side=tk.LEFT, padx=(5,0), pady=(50,5))

# Create a Label to display the capture panel
panel = tk.Label(capture_frame)
panel.pack()

# Create style for the sliders
style = Style(theme='vapor')

# Create trackbars for adjusting brightness
brightness_label = ttk.Label(root, text="Brightness", style='info.TLabel')
brightness_label.pack(padx=10,pady=(50,0))
brightness_scale = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, style="TScale")
brightness_scale.set(50)
brightness_scale.pack()

# Create trackbars for adjusting contrast
contrast_label = ttk.Label(root, text="Contrast", style='info.TLabel')
contrast_label.pack(padx=10,pady=(20,0))
contrast_scale = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, style="TScale")
contrast_scale.set(50)
contrast_scale.pack()

# Create trackbars for adjusting saturation
saturation_label = ttk.Label(root, text="Saturation", style='info.TLabel')
saturation_label.pack(padx=10,pady=(20,0))
saturation_scale = ttk.Scale(root,from_=0, to=100, orient=tk.HORIZONTAL, style="TScale")
saturation_scale.set(50)
saturation_scale.pack()

# Create a check button for auto enhance
auto_enhance_var = tk.IntVar()
auto_enhance_check = ttk.Checkbutton(root, text="Auto Enhance", variable=auto_enhance_var, onvalue=1, offvalue=0)
auto_enhance_check.pack(padx=10,pady=(20,0))

# Create a save button
save_button = ttk.Button(root, text="Capture", command=save_image, style='success.Outline.TButton')
save_button.pack(padx=10,pady=(270,0))

# Call the update_image_adjustments function to start the processing
update_image_adjustments()

# Start the Tkinter event loop
root.mainloop()

# Release the VideoCapture object
cap.release()
