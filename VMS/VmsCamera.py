from os import stat
from logger import log
import picamera
import serial
import time

DEFAULT_SAVE_DIR = './img/'
DEFAULT_BAUDRATE = 57600
DEFAULT_PORT = '/dev/ttyAMA0'
DEFAULT_TIMEOUT = 1

normal_res_img = './img/image1.jpg'
low_res_img = './img/img_lowres.jpg'
transfer_file = low_res_img

LOW_RESOLUTION = (160, 120)
DEFAULT_RESOLUTION = (320, 240)
HIGH_RESOLUTION = (640, 480)


class Error(Exception):
    pass

class VmsCamera:

    img_save_dir = DEFAULT_SAVE_DIR
    port = DEFAULT_PORT
    baudrate = DEFAULT_BAUDRATE
    timeout = DEFAULT_TIMEOUT
    resolution = DEFAULT_RESOLUTION

    def __init__(self, resolution=None, port=None, baudrate=None, timeout=None, img_save_dir=None):
        """
        - img_save_dir: directory where images should be saved
        """
        if resolution is not None:
            self.resolution = resolution
        if port is not None:
            self.port = port
        if baudrate is not None:
            self.baudrate = baudrate
        if timeout is not None:
            self.timeout = timeout
        if img_save_dir is not None:
            self.img_save_dir = img_save_dir

        if port is None: log.warn(f"Port is set to default value: {self.port}")
        if baudrate is None: log.warn(f"Baudrate is set to default value: {self.baudrate}")

        self.ser = self._init_serial()
        log.info(f"VmsCamera created!")
        self._init_camera()
        self._display_settings()

    def _init_camera(self):
        """
        Start the camera.
        Camera parameters are set at the constructor and the camera creation
        is thus not callable after the VMSCamera is created
        """
        try:
            log.info("Creating camera (PiCamera)")
            camera = picamera.PiCamera()
            log.info(f"Setting camera resolution: {self.resolution}")
            camera.resolution = self.resolution
            time.sleep(1)
            log.info("Camera started")
            self.camera = camera
        except:
            raise Error(f"There was an error starting the camera")

    def _init_serial(self):
        """ Initialize the serial communication """
        try:
            ser = serial.Serial(port = self.port, baudrate = self.baudrate, timeout = self.timeout)
            return ser
        except:
            raise Error("There was an error initializing the serial communications!")

    def _display_settings(self):
        """ Display the settings for the camera """
        print(f"""-- Camera settings --
        Resolution: {self.resolution}
        Port: {self.port}
        Baudrate: {self.baudrate}
        Timeout: {self.timeout}
        """)

    def transfer_file(self, file, chunk_size=1024):
        """
        Transfer file

        - file: the file to be transmitted
        - chunk_size: the size of the chunk to be transmitted each transmission
        """
        ser = self.ser
        if ser:
            with open(file, 'rb') as tfile:
                print(f"Starting transfer: {file}, chunk size: {chunk_size}")
                transfer_begin = time.perf_counter()

                filesize = self.estimate_filesize(file)

                while True:
                    chunk = tfile.read(chunk_size)
                    chunk_len = len(chunk)
                    if not chunk:
                        print("No chunks left, sending transfer complete...")
                        break
                    print(f"Sending chunk | length: {chunk_len}")
                    print(f"Chunk:\n{chunk}\n")
                    ser.write(chunk)
                    # time.sleep(0.01)

                transfer_finish = time.perf_counter()
                time_spent = transfer_finish - transfer_begin
                log.info(f"[!] Transfer complete | {filesize / 1024.0} kB in {time_spent} seconds")

    def estimate_filesize(self, file):
        """ Estimate filesize in bytes """
        filesize_b = stat(file).st_size
        # filesize_kb = filesize_b / 1024.0
        return filesize_b

    def close_serial(self):
        """ Close serial port """
        if self.ser:
            print('[!] Shutting down serial')
            self.ser.close()

    def snap_photo(self, savepath = None):
        """ Take picture """
        camera = self.camera
        if camera:
            if savepath is None:
                savepath = self.img_save_dir + 'img.jpg'
            log.info("Taking photo...")
            camera.start_preview()
            time.sleep(2)
            camera.capture(savepath)
            camera.stop_preview()
            log.info(f"Photo saved to: {savepath}")
            return savepath
        return None

    def snap_and_send_photo(self, chunk_size, savepath = None):
        """
        Take a photo and send it if everything goes well
        If the savepath is 'None' the default path will be set inside of 'snap_photo'
        """
        img = self.snap_photo(savepath)
        if img:
            self.transfer_file(file = img, chunk_size = chunk_size)

    def test_uart_transmission(self, test_length = 15):
        """ UART data transmission used for tests """
        ser = self.ser
        if ser:
            i = 0
            while i < test_length:
                ser.write(b"dummy data")
                time.sleep(1)


