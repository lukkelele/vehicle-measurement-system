import sys; import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import VMSCamera

save_dir = './img/'
baudrate = 57600
port = '/dev/ttyAMA0'
timeout = 1
test_length = 30
chunk_size = 1024

default_resolution = (320, 240)
low_res = (240, 180)
lower_res = (160, 120)
lowest_res = (80, 40)
resolution = lower_res


print("Starting VMSCamera test\n")
print("Setting up the camera...")

cam = VMSCamera.VMSCamera(resolution = resolution,
                          port = port,
                          baudrate = baudrate,
                          timeout = timeout)

print("Testing snapping photo and sending it...")
cam.snap_and_send_photo(chunk_size=chunk_size)
print("Exiting snap_and_send_photo()!")

# print(f"Starting to transmit dummy data for {test_length/2} seconds")
# cam.test_uart_transmission(test_length=test_length)


print("VMSCamera test complete!\nExiting...")
