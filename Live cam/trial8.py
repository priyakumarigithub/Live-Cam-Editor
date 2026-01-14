#color and UI modified


import cv2
import numpy as np
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
from ttkbootstrap import Style
import os

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

    # Adjust the saturation of the frame
    adjusted_frame[:, :, 1] = np.clip((adjusted_frame[:, :, 1] * saturation), 0, 255).astype(np.uint8)

    # Convert the adjusted frame back to BGR color space
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_HSV2BGR)

    # Convert the adjusted frame to RGB color space
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2RGB)

    # Convert the adjusted frame to grayscale
    gray = cv2.cvtColor(adjusted_frame, cv2.COLOR_RGB2GRAY)

    # Calculate the histogram using OpenCV
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    # Normalize the histogram
    hist = cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)

    # Create a blank image for displaying the histogram
    hist_image = np.zeros((200, 256, 3), dtype=np.uint8)

    # Plot the histogram on the blank image
    hist_height = hist_image.shape[0]
    hist_width = hist_image.shape[1]
    bin_width = int(hist_width / 256)
    for i in range(256):
        bin_height = int(hist[i] * hist_height / np.max(hist))
        cv2.rectangle(hist_image, (i * bin_width, hist_height), ((i + 1) * bin_width, hist_height - bin_height),
                      (255, 255, 255), -1)

    # Resize the histogram image to match the width of the adjusted frame
    hist_image_resized = cv2.resize(hist_image, (adjusted_frame.shape[1], hist_image.shape[0]))

    # Combine the adjusted frame and histogram
    combined = np.vstack((adjusted_frame, hist_image_resized))

    # Convert the combined image to PIL format
    combined_image = Image.fromarray(combined)

    # Convert the PIL image to Tkinter format
    combined_tk_image = ImageTk.PhotoImage(image=combined_image)

    # Update the image in the panel
    panel.config(image=combined_tk_image)
    panel.image = combined_tk_image  # Store a reference to avoid garbage collection

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
    brightness = np.argmax(cdf > 0.01) / 2 + 25
    contrast = (np.argmax(cdf > 0.50) - np.argmax(cdf > 0.05)) / 2
    saturation = np.argmax(cdf > 0.1) / 2 + 25

    return brightness, contrast, saturation

# Function to save the current image displayed in the panel
def save_image():
    # Read the frame from the camera
    frame = cap.read()

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

# Create a VideoCapture object to read from the camera
cap = cv2.VideoCapture(0)  # 0 represents the default camera

# Create a Tkinter window
root = tk.Tk()
root.title("Camera and Histogram")
root.resizable(width=False, height=False)
root.configure(background='')

# Create a Frame to hold the capture panel and save button
capture_frame = tk.Frame(root)
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
