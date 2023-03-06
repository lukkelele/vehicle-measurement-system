import time
import picamera
import serial

WIDTH, HEIGHT = 640, 480
PI_VIDEO_PATH = '/home/pi/Videos/video.h264'
VIDEO_DURATION = 10

# Set UART connection details
UART_ENABLED = False
BAUDRATE = 115200
UART_PORT = '/dev/ttyUSB0'
TIMEOUT = 1

def init_camera(width = WIDTH, height = HEIGHT):
    print('Starting camera...\nResolution: %dx%d' % (WIDTH, HEIGHT))
    # Initialize the camera
    camera = picamera.PiCamera()
    camera.resolution = (WIDTH, HEIGHT)
    camera.start_preview()
    time.sleep(2)
    return camera

# Shutdown the camera
def camera_shutdown(camera):
    camera.stop_recording()
    camera.stop_preview()
    camera.close()

# Record a video and save the footage to @savepath
def record_video(savepath):
    camera.start_recording(savepath)
    camera.wait_recording(VIDEO_DURATION)

def transmit_data(path = PI_VIDEO_PATH, uart_port = UART_PORT, baud = BAUDRATE, timeout = TIMEOUT):
    ser = serial.Serial(uart_port, baud, timeout=1)

    with open('/home/pi/Desktop/video.h264', 'rb') as f:
        data = f.read()
        ser.write(data)

    ser.close()



camera = init_camera()

record_video(PI_VIDEO_PATH)

camera_shutdown(camera)


