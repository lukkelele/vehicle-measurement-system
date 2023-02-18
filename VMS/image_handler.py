import cv2
import numpy as np

# Load the image
img = cv2.imread('car.jpg', cv2.IMREAD_GRAYSCALE)

# Apply Canny edge detection to find the edges
edges = cv2.Canny(img, 100, 200)

# Find contours of the car
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Get the largest contour
largest_contour = max(contours, key=cv2.contourArea)

# Get the bounding rectangle of the contour
x,y,w,h = cv2.boundingRect(largest_contour)

# Calculate the length of the car in pixels
car_length_pixels = w

# Define a conversion factor to convert pixel length to real-world length
# This will depend on the camera calibration and distance from the car
conversion_factor = 0.1 # 1 pixel = 0.1 meters

# Calculate the length of the car in meters
car_length_meters = car_length_pixels * conversion_factor

# Print the result
print("Car length: %.2f meters" % car_length_meters)
