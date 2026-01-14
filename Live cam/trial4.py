import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Function to update the brightness, contrast, and saturation values based on the trackbar positions
def update_image_adjustments():
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

    # Apply the brightness, contrast, and saturation adjustments to the camera frame
    adjusted_frame = np.clip((frame * contrast + brightness), 0, 255).astype(np.uint8)
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2HSV)

    # Adjust the saturation of the frame
    adjusted_frame[:, :, 1] = np.clip((adjusted_frame[:, :, 1] * saturation), 0, 255).astype(np.uint8)

    # Convert the adjusted frame back to BGR color space
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_HSV2BGR)

    # Convert the adjusted frame to RGB color space
    adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2RGB)

    # Calculate the histogram using OpenCV
    gray = cv2.cvtColor(adjusted_frame, cv2.COLOR_RGB2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    # Normalize the histogram
    hist = cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)

    # Create a blank image for displaying the histogram
    hist_image = np.zeros((adjusted_frame.shape[0], 256, 3), dtype=np.uint8)

    # Resize the histogram image
    hist = np.reshape(hist, (256,))
    hist_image = cv2.resize(hist_image, (256, adjusted_frame.shape[0]))

    # Plot the histogram on the blank image
    for i in range(256):
        cv2.line(hist_image, (i, hist_image.shape[0]), (i, hist_image.shape[0] - int(hist[i])), (255, 255, 255))

    # Combine the adjusted frame and histogram side by side
    combined = np.hstack((adjusted_frame, hist_image))

    # Convert the combined image to PIL format
    combined_image = Image.fromarray(combined)

    # Convert the PIL image to Tkinter format
    combined_tk_image = ImageTk.PhotoImage(image=combined_image)

    # Update the image in the panel
    panel.config(image=combined_tk_image)
    panel.image = combined_tk_image  # Store a reference to avoid garbage collection

    # Schedule the next update
    root.after(20, update_image_adjustments)


# Create a VideoCapture object to read from the camera
cap = cv2.VideoCapture(0)  # 0 represents the default camera

# Create a Tkinter window
root = tk.Tk()
root.title("Camera and Histogram")
root.resizable(width=False, height=False)
root.configure(background='#333333')

# Create a Frame to hold the capture panel
capture_frame = tk.Frame(root)
capture_frame.pack(side=tk.LEFT, padx=0, pady=0)

# Create a Frame to hold the histogram
histogram_frame = tk.Frame(root)
histogram_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Create a Label to display the capture panel
panel = tk.Label(capture_frame)
panel.pack()

# Create style for the sliders
style = ttk.Style()
style.configure("TScale", sliderlength=100, background='#333333')  # Adjust the slider length

# Create trackbars for adjusting brightness
brightness_label = tk.Label(histogram_frame, text="Brightness")
brightness_label.pack()
brightness_scale = ttk.Scale(histogram_frame, from_=0, to=100, orient=tk.HORIZONTAL, style="TScale")
brightness_scale.set(50)
brightness_scale.pack()

# Create trackbars for adjusting contrast
contrast_label = tk.Label(histogram_frame, text="Contrast")
contrast_label.pack()
contrast_scale = ttk.Scale(histogram_frame, from_=0, to=100, orient=tk.HORIZONTAL, style="TScale")
contrast_scale.set(50)
contrast_scale.pack()

# Create trackbars for adjusting saturation
saturation_label = tk.Label(histogram_frame, text="Saturation")
saturation_label.pack()
saturation_scale = ttk.Scale(histogram_frame, from_=0, to=100, orient=tk.HORIZONTAL, style="TScale")
saturation_scale.set(50)
saturation_scale.pack()

# Call the update_image_adjustments function to start the processing
update_image_adjustments()

# Start the Tkinter event loop
root.mainloop()

# Release the VideoCapture object
cap.release()
