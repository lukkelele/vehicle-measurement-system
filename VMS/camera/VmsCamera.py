from os import stat
import picamera
import serial
import time

DEFAULT_SAVE_DIR = './img'
DEFAULT_BAUDRATE = 115200
DEFAULT_PORT = '/dev/ttyAMA0'
DEFAULT_TIMEOUT = 1

chunk_sizes = {
    'small': 1024,
    'normal': 2048,
    'large': 4096 
}

# Byte sizes -> bytes, kilobytes, megabytes
byte_types = {
    'b': 0,
    'kb': 1,
    'mb': 2
}

normal_res_img = './img/image1.jpg'
low_res_img = './img/img_lowres.jpg'
transfer_file = low_res_img

class Error(Exception):
    pass

class VmsCamera:

    img_save_dir = DEFAULT_SAVE_DIR
    baudrate = DEFAULT_BAUDRATE

    def __init__(self, port=None, baudrate=None, img_save_dir=None):
        """
        - img_save_dir: directory where images should be saved
        """
        if port is not None:
            self.port = port
        if baudrate is not None:
            self.baudrate = baudrate
        if img_save_dir is not None:
            self.img_save_dir = img_save_dir 

        self.ser = self._init_serial()

    def _init_serial(self, port, baudrate):
        """
        Initialize the serial communication
        If either port or baudrate passed as arguments are None then set default values
        """
        try:
            if port is None:
                port = self.port
                print(f"Port is set to default value -> {self.port}")

            if baudrate is None:
                baudrate = self.baudrate
                print(f"Baudrate is set to default value -> {self.baudrate}")

            print(f"Setting up serial communications:\nPort: {port}\nBaudrate: {baudrate}")
            ser = serial.Serial(port = port,
                                baudrate = baudrate,
                                timeout = DEFAULT_TIMEOUT)
            return ser
        except:
            raise Error("There was an error initializing the serial communications!")

    def transfer_file(self, file, chunk_size=4096):
        """
        Transfer file

        - file: the file to be transmitted
        """
        if self.ser:
            with open(file, 'rb') as tfile:
                print(f"Starting transfer: {file}, chunk size: {chunk_size}")
                transfer_begin = time.perf_counter()
                filesize = self.estimate_filesize(file)
                while True:
                    chunk = tfile.read(chunk_size)
                    if not chunk:
                        # end of line
                        print("No chunks left, leaving...")
                        break
                    print("Sending chunk")
                    self.ser.write(chunk)
                transfer_finish = time.perf_counter()
                time_spent = transfer_begin - transfer_finish
                print(f"[!] Transfer complete | {filesize} kB in {time_spent} seconds")


    def estimate_filesize(self, file):
        """Estimate filesize in kilobytes"""
        filesize_b = stat(file)
        filesize_kb = filesize_b / 1024.0
        return filesize_kb


    def close_serial(self):
        """Close serial port"""
        if self.ser: 
            print('[!] Shutting down serial')
            self.ser.close()

    def snap_photo(self):
        """Take a picture"""

