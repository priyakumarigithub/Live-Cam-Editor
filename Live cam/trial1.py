#Live cam and Histogram Working


import cv2
import numpy as np
import matplotlib.pyplot as plt

# Create a VideoCapture object to read from the camera
cap = cv2.VideoCapture(0)  # 0 represents the default camera

while True:
    # Read the frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate the histogram using OpenCV
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    # Normalize the histogram
    hist = cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)

    # Create a blank image for displaying the histogram
    hist_image = np.zeros((frame.shape[0], 256, 3), dtype=np.uint8)

    # Resize the histogram image
    hist = np.reshape(hist, (256,))
    hist_image = cv2.resize(hist_image, (256, frame.shape[0]))

    # Plot the histogram on the blank image
    for i in range(256):
        cv2.line(hist_image, (i, hist_image.shape[0]), (i, hist_image.shape[0] - int(hist[i])), (255, 255, 255))

    # Combine the camera frame and histogram side by side
    combined = np.hstack((frame, hist_image))

    # Display the combined image
    cv2.imshow('Camera and Histogram', combined)

    # Check for the 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
