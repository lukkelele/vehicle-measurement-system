from cv2 import cv2 as cv
import socket

BIND_IP_ADDR = 'localhost' # TODO: pass cameras socket ip here
BIND_PORT = 8000
WIDTH = 640
HEIGHT = 480
FRAMERATE = 30
COLOR_FORMAT = 'bgr'
VIDEO_FILENAME = 'VIDEO_OUTPUT.avi'

class Computer:
    def __init__(self, bind_ip=BIND_IP_ADDR, port=BIND_PORT):
        self.bind_ip = bind_ip
        self.bind_port = port
        
    def connect(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen()
        self.conn, self.addr = self.sock.accept()

    def create_videostream(self, video_format='XVID'):
        self.stream = cv.VideoWriter_fourcc(*video_format)
        self.out = cv.VideoWriter(VIDEO_FILENAME, self.stream, FRAMERATE,
                                  (WIDTH, HEIGHT))
