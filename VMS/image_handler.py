from enum import Enum
import cv2 as cv
import numpy as np
import math

class rgb_color(Enum):
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)

car_image = '../img/red_car.jpg'
# car_image = '../img/drive-by.jpg'
# car_image = '../img/crime-scene.jpg'

# Get bounding box for an image
# TODO: Add parameters for varying threshold values
def get_bounding_box(img):
    font_color = (0, 255, 0)
    box_color = rgb_color.green.value
    font_color = box_color # Set font and rectangle to same color
    image = cv.imread(img) 
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5,5), 0)
    thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    x,y,w,h = cv.boundingRect(thresh)
    cv.rectangle(image, (x, y), (x + w, y + h), box_color, 2)
    cv.putText(image, "w={},h={}".format(w,h), (x,y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.7, font_color, 2)
    cv.imshow('tresh', thresh)
    cv.imshow('image', image)
    cv.waitKey()

get_bounding_box(car_image)
  

# Detect cars using a trained XML classifier
def detect_cars(video_path):
    car_cascade = cv.CascadeClassifier('cars.xml')
    video_capture = cv.VideoCapture(video_path)

    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            print('[ERROR] Frame couldn\'t be handled')
            break

        # Grayscale conversion
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cars = car_cascade.detectMultiScale(gray, 1.1, 1)

        for (x, y, w, h) in cars:
            cv.rectangle(frame, (x, y), (x + w, y + h), rgb_color.green.value, 2)
      
        cv.imshow('Frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
      
    video_capture.release()
    cv.destroyAllWindows()

