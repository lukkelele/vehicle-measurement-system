from cv2 import cv2 as cv
import numpy as np
import socket
import picamera

# Unencoded format rounds up the request resolution
# Horizontal rounds to the nearest multiple of 32 
# Vertical rounds to the nearest multiple of 16

IP_ADDR = 'localhost'
PORT = 8000
WIDTH = 640
HEIGHT = 480
FRAMEWRATE = 30
COLOR_FORMAT = 'bgr'


class Camera:

    def __init__(self, width=WIDTH, height=HEIGHT, framerate=FRAMEWRATE,
                 ip_addr=IP_ADDR, port=PORT, color_format=COLOR_FORMAT):
        self.width, self.height = width, height
        self.framerate = framerate
        self.color_format = color_format
        # Create the socket and connect it
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(ip_addr, port)
        self.camera = picamera.PiCamera()
        self.output = np.empty((self.width, self.height, 3), dtype=np.uint8)

    def connect(self, ip, port):
        self.sock.connect((ip, port))

    def create_videostream(self, video_format='XVID', filename='camvid.avi'):
        self.stream = cv.VideoWriter_fourcc(*video_format)
        self.out = cv.VideoWriter(filename, self.stream, self.framerate, 
                                  (self.width, self.height))

    def capture_image(self):
        frame = self.camera.capture(self.output, self.color_format)
        image = self.output.reshape((self.width, self.height, 3))
        return image

    def stream_data(self):
        # Get image
        image = self.capture_image()
        # FIXME: Send frame
        self.sock.sendall(image)
        # Output frame to video file
        self.out.write(image)
