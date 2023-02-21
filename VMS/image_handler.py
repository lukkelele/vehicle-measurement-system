from PIL import Image
from enum import Enum
from time import sleep
import cv2 as cv
import numpy as np
import math

class rgb_color(Enum):
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)

LOCAL_DIR_IMAGES = "../img"
car_image = '../img/red_car.jpg'
# car_image = '../img/drive-by.jpg'
# car_image = '../img/crime-scene.jpg'

# TODO: Add parameters for varying threshold values
def get_bounding_box(img: str):
    """
    Get bounding box for an image
    img: path to image
    """
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


def save_image(img: str):
    """ 
    Save an image locally
    img: image element provided by the webdriver
    img_name: name of saved image
    returns: 1 for successful file write, 0 for error
    """
    # TODO: Add functionality to save to other paths
    img_name = LOCAL_DIR_IMAGES + img
    print("Saving image: %s" % img_name)
    try:
        with open(img_name, 'wb') as file:
            file.write(img_name)
        return 1
    except:
        print("There was an error saving an image: %s" % img_name)
        return 0

def crop_image(img_name: str, position: tuple, size: tuple):
    """
    Read an image, crop it and save it as a copy
    
    img_path: path to directory with the images
    position: the positioning of the image on the page in pixels
    size: tuple with the (width, height)
    returns: 1 for successful file write, 0 for error
    """
    img_path = LOCAL_DIR_IMAGES + img_name
    img = cv.imread(img_path)
    x, y = position
    w, h = size
    try:
        crop_img = img[y:y+h, x:x+w]
        img_name = img_path[:-4]
        # 'i' is the number of the img and img_name[:6] is sliced './img/'
        i = img_path[-5]
        img_name = img_name + "_crop.png"
        print(f"Cropping image: {img_name}")
        cv.imwrite(img_name, crop_img)
        sleep(0.35)
        return 1
    except:
        print("There was an error cropping the image")
        return 0


def detect_cars(video_path: str):
    """
    Detect cars in the frames of a video using a trained XML classifier
    """
    car_cascade = cv.CascadeClassifier('cars.xml')
    video_capture = cv.VideoCapture(video_path)

    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            print('[ERROR] Frame couldn\'t be handled')
            break

        # Grayscale conversion FIXME: Clean this up using functions
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cars = car_cascade.detectMultiScale(gray, 1.1, 1)

        for (x, y, w, h) in cars:
            cv.rectangle(frame, (x, y), (x + w, y + h), rgb_color.green.value, 2)
      
        cv.imshow('Frame', frame)
        if cv.waitKey(1) == ord('q'):
            break

    # Cleanup before leaving function
    video_capture.release()
    cv.destroyAllWindows()


def gray_image(image):
    """ Convert an image to grayscale """
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return gray_image


def reduce_noise(image):
    """ Reduce noise in grayscale image """
    x, y, z = 11, 17, 17
    image = cv.bilateralFilter(image, x, y, z) 
    return image


def detect_edges(image, a = 30, b = 200):
    """ Detect edges in image """
    image = cv.Canny(image, a, b)
    return image


def gray_reduce_img(image):
    """ Reduce noise and gray out an image """
    return reduce_noise(gray_image(image))


def detect_contours(image):
    """
    Detect contours in picture 
    Return a cropped version
    """
    screenContour = None
    contours, new = cv.findContours(image.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    # Pick 30 contours with the smallest area
    contours = sorted(contours, key=cv.contourArea, reverse=True)[:30]
    # Find contour with four sides -> RECTANGLE 
    for c in contours: 
        perimeter = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.018 * perimeter, True)

        if len(approx) == 4:
            screenContour = approx 
            # Crop rectangle area
            x, y, w, h = cv.boundingRect(c)
            img = image[y:y+h, x:x+w]
            return img

    img_copy = image.copy()
    cv.drawContours(img_copy, [screenContour], -1, (0, 255, 0), 3)
    return img_copy, contours


def process_img(img: str):
    """
    Process an image in the following manner:
    Normalize -> threshold -> gaussian blur -> grayscale -> noise -> edges -> contours
    """
    org_image = cv.imread(img)
    #org_image = imutils.resize(org_image, width=300, height=300)
    np_img = np.array(Image.open(img))
    norm_img = np.zeros((np_img.shape[0], np_img.shape[1]))
    img = cv.normalize(org_image, norm_img, 0, 255, cv.NORM_MINMAX)
    img = cv.threshold(img, 100, 255, cv.THRESH_BINARY)[1]
    img = cv.GaussianBlur(img, (1,1), 0)
    #cv2.imshow("img", img); cv2.waitKey(0)
    #gray_image = gray_image(org_image)
    grayed_image = gray_image(img)
    noise_image = reduce_noise(grayed_image)
    edge_image = detect_edges(noise_image)
    contours_image, cnts = detect_contours(edge_image)
    return contours_image, cnts

# get_bounding_box(car_image)
