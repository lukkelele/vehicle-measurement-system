import time
import picamera

low_resolution = (320, 240)

WIDTH = 640
HEIGHT = 480

print('Starting the camera...')
# Setup the camera
camera = picamera.PiCamera()
# camera.resolution = (WIDTH, HEIGHT)
camera.resolution = low_resolution
camera.start_preview()

time.sleep(2.5)
print('Capturing image...')
# Capture image
camera.capture('/home/pi/Code/VMS/img/img_lowres.jpg')
camera.stop_preview()
print('Stopping preview')

# Stop the camera
camera.close()
print('Camera closed! Exiting')
