from logger import log
from os import stat
import picamera
import serial
import time

UART_ID = 0
BAUDRATE = 115200
CHUNKSIZE = 4096
TIMEOUT = 10
PI_PORT = "/dev/ttyAMA0"
SAVE_DIR = "./img/"

LOW_RESOLUTION = (160, 120)
DEFAULT_RESOLUTION = (320, 240)
HIGH_RESOLUTION = (640, 480)

class Error(Exception):
    pass

class VMSCamera:

    img_save_dir = "./img/"
    port = PI_PORT
    baudrate = BAUDRATE
    timeout = TIMEOUT
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

    def transfer_file(self, file, chunksize=1024):
        """
        Transfer file

        - file: the file to be transmitted
        - chunksize: the size of the chunk to be transmitted each transmission
        """
        ser = self.ser
        if ser:
            with open(file, 'rb') as tfile:
                print(f"Starting transfer: {file}, chunk size: {chunksize}")
                transfer_begin = time.perf_counter()

                # TODO: Fix this for file size syncing
                filesize = self.estimate_filesize(file)
                filesize_b = filesize.to_bytes(4, "big")
                print(f"Filesize: {filesize}\nFilesize (bytes): {filesize_b}")
                ser.write(filesize_b)

                while True:
                    chunk = tfile.read(chunksize)
                    chunk_len = len(chunk)
                    if not chunk:
                        print("No chunks left, sending transfer complete...")
                        break
                    print(f"Sending chunk | length: {chunk_len}")
                    # print(f"Chunk:\n{chunk}\n")
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

    def snap_and_send_photo(self, chunksize = None, savepath = None):
        """
        Take a photo and send it if everything goes well
        If the savepath is 'None' the default path will be set inside of 'snap_photo'
        """
        if chunksize is None:
            chunksize = CHUNKSIZE
        img = self.snap_photo(savepath)
        if img:
            self.transfer_file(file = img, chunksize = chunksize)
