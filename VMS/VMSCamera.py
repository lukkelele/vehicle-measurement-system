from os import stat
import picamera
import VMSlib
import logger
import serial
import time

UART_ID = 0
BAUDRATE = 115200
CHUNKSIZE = 4096
TIMEOUT = 10
PI_PORT = "/dev/ttyAMA0"
IMAGE_SAVE_DIR = "./img/"

LOW_RESOLUTION = (160, 120)
DEFAULT_RESOLUTION = (320, 240)
HIGH_RESOLUTION = (640, 480)


class VMSCamera:

    img_save_dir = IMAGE_SAVE_DIR
    port = PI_PORT
    baudrate = BAUDRATE
    timeout = TIMEOUT
    resolution = DEFAULT_RESOLUTION
    log = logger.Logger("VMSCamera")
    debuglevel = 1

    def __init__(self, resolution=None, serial_port=None, baudrate=None, timeout=None, img_save_dir=None):
        """
        - img_save_dir: directory where images should be saved
        """
        if resolution is not None: self.resolution = resolution
        if serial_port is not None: self.serial_port = serial_port
        if baudrate is not None: self.baudrate = baudrate
        if timeout is not None: self.timeout = timeout
        if img_save_dir is not None: self.img_save_dir = img_save_dir
        if serial_port is None: log.warn(f"Port is set to default value: {self.serial_port}")
        if baudrate is None: log.warn(f"Baudrate is set to default value: {self.baudrate}")

        self.ser = self._init_serial()
        self._init_camera()
        self.log.info(f"VMSCamera created!")
        self.display_settings()

    def _init_camera(self):
        """
        Start the camera.
        Camera parameters are set at the constructor and the camera creation
        is thus not callable after the VMSCamera is created
        """
        try:
            camera = picamera.PiCamera()
            camera.resolution = self.resolution
            time.sleep(1)
            self.camera = camera
        except:
            raise VMSlib.ConstructorError(f"There was an error starting the camera")

    def _init_serial(self):
        """ Initialize the serial communication """
        try:
            ser = serial.Serial(port = self.serial_port, baudrate = self.baudrate, timeout = self.timeout)
            return ser
        except:
            raise VMSlib.SerialInterfaceStartupError("There was an error initializing the serial communications!")

    def display_settings(self):
        """ Display the settings for the camera """
        print(f"""---- Camera settings ----
    Resolution: {self.resolution}
    Serial Port: {self.serial_port}
    Baudrate: {self.baudrate}
    Timeout: {self.timeout}
        """)

    def transfer_file(self, file, chunksize):
        """
        Transfer file

        - file: the file to be transmitted
        - chunksize: the size of the chunk to be transmitted each transmission
        """
        ser = self.ser
        if ser:
            with open(file, "rb") as tfile:
                transfer_begin = time.perf_counter()
                filesize = self.estimate_filesize(file)
                filesize_b = filesize.to_bytes(4, "big")
                self.log.info(f"Sending the filesize of {filesize} bytes")
                ser.write(filesize_b)

                self.log.info("File transfer started...")
                # TODO: Add 'transfer' - bar for progress
                while True:
                    # Read data with a size of 'chunksize'
                    chunk = tfile.read(chunksize)
                    chunk_len = len(chunk)

                    # If no data to read left, stop sending
                    if not chunk:
                        self.log.info("No chunks left, sending transfer complete...")
                        break

                    # Send the data over the serial connection
                    # self.log.info(f"Sending chunk | length: {chunk_len}")
                    self.log
                    ser.write(chunk)

                # Output a log statement with file transfer information
                transfer_finish = time.perf_counter()
                time_spent = transfer_finish - transfer_begin
                self.log.info(f"File transfer complete! Sent {filesize / 1024.0} kB in {time_spent} seconds\n")

    def estimate_filesize(self, file):
        """ Estimate filesize in bytes """
        filesize_b = stat(file).st_size
        # filesize_kb = filesize_b / 1024.0
        return filesize_b

    def close_serial(self):
        """ Close serial port """
        if self.ser:
            self.log.warn('Shutting down serial connection')
            self.ser.close()

    def snap_photo(self, savepath = None):
        """ Take picture """
        camera = self.camera
        if camera:
            if savepath is None: 
                savepath = self.img_save_dir

            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            file_loc = f"{savepath}/{timestamp}.jpg"

            self.log.info("Snapping photo...")
            camera.start_preview()
            time.sleep(2)
            camera.capture(file_loc)
            camera.stop_preview()
            # self.log.info(f"Photo saved to: {file_loc}")

            return file_loc
        return None

    def snap_and_send_photo(self, chunksize = None, savepath = None):
        """
        Take a photo and send it if everything goes well
        If the savepath is 'None' the default path will be set inside of 'snap_photo'
        """
        if chunksize is None: 
            chunksize = CHUNKSIZE

        # Take photo and if the photo was correctly saved, transfer it on the
        # serial connection
        img = self.snap_photo(savepath)
        if img:
            self.transfer_file(file = img, chunksize = chunksize)
