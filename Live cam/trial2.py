#Live cam and Histogram with brightness and contrast slider


import cv2
import numpy as np

# Function to update the brightness and contrast values based on the trackbar positions
def update_brightness_contrast(brightness, contrast):
    # Convert the brightness and contrast values from trackbar positions to actual values
    brightness = (brightness - 50) * 2
    contrast = contrast / 50.0

    # Apply the brightness and contrast adjustments to the camera frame
    adjusted_frame = np.clip((frame * contrast + brightness), 0, 255).astype(np.uint8)

    # Convert the adjusted frame to grayscale
    gray = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2GRAY)

    # Calculate the histogram using OpenCV
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

    # Display the combined image
    cv2.imshow('Camera and Histogram', combined)


# Create a VideoCapture object to read from the camera
cap = cv2.VideoCapture(0)  # 0 represents the default camera

# Create a window to display the combined image
cv2.namedWindow('Camera and Histogram')

# Create trackbars for adjusting brightness and contrast
cv2.createTrackbar('Brightness', 'Camera and Histogram', 50, 100, lambda x: None)
cv2.createTrackbar('Contrast', 'Camera and Histogram', 50, 100, lambda x: None)

while True:
    # Read the frame from the camera
    ret, frame = cap.read()

    # Get the current trackbar positions for brightness and contrast
    brightness = cv2.getTrackbarPos('Brightness', 'Camera and Histogram')
    contrast = cv2.getTrackbarPos('Contrast', 'Camera and Histogram')

    # Update the brightness and contrast values
    update_brightness_contrast(brightness, contrast)

    # Check for the 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
