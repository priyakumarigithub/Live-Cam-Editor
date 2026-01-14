#Auto Enhance
'''
logic used in the calculate_auto_enhance function:

Convert the frame to grayscale: This step is performed to simplify the histogram calculation. By converting the frame to grayscale, we can focus on the intensity values rather than individual color channels.

Calculate the histogram: The histogram represents the distribution of pixel intensities in the grayscale image. It counts the number of pixels at each intensity level (0-255).

Calculate the cumulative distribution function (CDF) of the histogram: The CDF provides information about the cumulative proportion of pixels below a given intensity level. It is calculated by dividing the cumulative sum of histogram values by the total sum of histogram values.

Calculate the auto enhance values:

Brightness: The brightness value is determined by finding the intensity level at which the cumulative distribution function (CDF) exceeds a threshold (0.05 in this case). The resulting brightness value is scaled and adjusted to a range of 25-100.
Contrast: The contrast value is calculated as the difference between the intensity level where the CDF exceeds a higher threshold (0.95) and the intensity level where the CDF exceeds the lower threshold (0.05). The resulting contrast value represents the range of intensities spanned between these two thresholds.
Saturation: The saturation value is determined by finding the intensity level at which the cumulative distribution function (CDF) exceeds a threshold (0.5 in this case). The resulting saturation value is scaled and adjusted to a range of 25-100.
Return the auto enhance values: The calculated brightness, contrast, and saturation values are returned from the function.

By calculating the auto enhance values based on the histogram and CDF, the function aims to determine suitable adjustments for brightness, contrast, and saturation that enhance the visual quality of the image. These values can then be used to automatically adjust the image's appearance.
'''


import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
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

# Create a VideoCapture object to read from the camera
cap = cv2.VideoCapture(0)  # 0 represents the default camera

# Create a Tkinter window
root = tk.Tk()
root.title("Camera and Histogram")
root.resizable(width=False, height=False)
root.configure(background='#333333')

# Create a Frame to hold the capture panel and save button
capture_frame = tk.Frame(root)
capture_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Create a Label to display the capture panel
panel = tk.Label(capture_frame)
panel.pack()

# Create style for the sliders
style = ttk.Style()
style.configure("TScale", sliderlength=100, background='#333333')

# Create trackbars for adjusting brightness
brightness_label = tk.Label(root, text="Brightness", bg='#333333', fg='white')
brightness_label.pack()
brightness_scale = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, style="TScale")
brightness_scale.set(50)
brightness_scale.pack()

# Create trackbars for adjusting contrast
contrast_label = tk.Label(root, text="Contrast", bg='#333333', fg='white')
contrast_label.pack()
contrast_scale = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, style="TScale")
contrast_scale.set(50)
contrast_scale.pack()

# Create trackbars for adjusting saturation
saturation_label = tk.Label(root, text="Saturation", bg='#333333', fg='white')
saturation_label.pack()
saturation_scale = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, style="TScale")
saturation_scale.set(50)
saturation_scale.pack()

# Create a check button for auto enhance
auto_enhance_var = tk.IntVar()
auto_enhance_check = ttk.Checkbutton(root, text="Auto Enhance", variable=auto_enhance_var, onvalue=1, offvalue=0)
auto_enhance_check.pack(padx=10, pady=10)

# Create a save button
save_button = ttk.Button(root, text="Save Image", command=save_image)
save_button.pack(padx=10, pady=10)

# Call the update_image_adjustments function to start the processing
update_image_adjustments()

# Start the Tkinter event loop
root.mainloop()

# Release the VideoCapture object
cap.release()
