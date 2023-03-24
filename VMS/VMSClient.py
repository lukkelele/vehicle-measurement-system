from machine import UART, Pin
from VMSlib import *
import pico_logger as log
import wifi as _wifi
import _secret as s
import socket
import time
import _thread

class VMSClient:
    UART_ID = 0
    BAUDRATE = 115200
    CHUNKSIZE = 4096
    TIMEOUT = 10
    ONBOARD_LED = Pin("LED", Pin.OUT)
    TX_PIN = Pin(0)
    RX_PIN = Pin(1)

    host = s.HOST_ADDR
    port = s.SOCK_PORT
    ssid = s.WIFI_SSID
    password = s.WIFI_PASSWORD
    wifi = None
    sock = None     # Data transmission socket
    logsock = None  # Logging socket
    uart = None
    uart_id = UART_ID
    baudrate = BAUDRATE
    timeout = TIMEOUT
    chunksize = CHUNKSIZE
    byteorder = "big"

    def __init__(self, host=None, port=None, ssid=None, password=None, timeout=None, 
                 uart_id=None, baudrate=None, chunksize=None, byteorder=None):
        if host is not None: self.host = host
        if port is not None: self.port = port
        if ssid is not None: self.ssid = ssid
        if timeout is not None: self.timeout = timeout
        if password is not None: self.password = password
        if chunksize is not None: self.chunksize = chunksize
        if byteorder is not None: self.byteorder = byteorder

        self.ONBOARD_LED.value(1)
        time.sleep(1.5)

        # Setup wifi connection on separate thread
        print('Starting new thread with wifi')
        _thread.start_new_thread(self.connect_to_wifi, (self.ssid, self.password))

        # Setup uart communication
        self.uart = self.init_uart(uart_id, baudrate)

        # Setup socket and connect to VMSServer
        if host and port: 
            self.sock = self.create_socket_connection(host=self.host, port=self.port, timeout=self.timeout)


    def create_socket_connection(self, host, port, timeout):
        try:
            sock = socket.socket()
            # sock.settimeout(timeout)
            sock_addr = socket.getaddrinfo(host, port)[0][-1]
            print("Sock addr: ", sock_addr)
            sock.connect(sock_addr)
            return sock
        except:
            raise SocketConnectionError(f"Could not create socket using: {host}:{port}, timeout: {timeout}")


    def connect_to_wifi(self, ssid, password):
        if self.wifi is not None:
            self.wifi.connect(ssid, password)
        else:
            ConnectionError(f"Wifi is NOT connected, current target: {ssid}")


    def init_uart(self, uart_id=None, baudrate=None):
        if uart_id is not None: self.uart_id = uart_id
        if baudrate is not None: self.baudrate = baudrate

        if not uart_id and not baudrate:
            log.warn("No UART id or baudrate was given, using default settings")
        return UART(self.uart_id, self.baudrate, parity=None, stop=1, bits=8, tx=self.TX_PIN, rx=self.RX_PIN)


    def recieve_uart_data(self):
        """ Saves all data to the onboard memory and returns the file in bytes """
        if self.uart:
            file = b""
            filesize = int.from_bytes(self.uart.read(4), self.byteorder)
            datasize = 0

            while filesize > datasize:
                data = self.uart.read(self.chunksize)
                if data is not None:
                    file += data
                datasize = len(file)

            return file

    def send_file_bytes(self, file: bytes):
        """
        Send file to server.
        Chunksize is automatically synced on the server to whatever is set in this function
        """
        if self.sock:
            chunksize = self.chunksize
            filesize = len(file)
            print("Filesize: ", filesize)

            # Send file size as the first 4 bytes to the server
            filesize_b = filesize.to_bytes(4, "big")
            self.sock.sendall(filesize_b)

            # Send the data
            for i in range(0, filesize, chunksize):
                self.sock.sendall(file[i : i + chunksize])

    def send_allocated_file(self):
        """
        Send a file using allocated memory instead of sending the file in a stream-like manner.
        """
        self.ONBOARD_LED.value(1)
        data = self.recieve_uart_data()
        self.send_file_bytes(data)

    def on_update(self):
        """
        On update function, to run every cycle
        Takes care of all that the pico has to do, polling, transmission etc
        """
        self.ONBOARD_LED.value(0)
        if self.sock and self.uart:
            if self.uart.any():
                self.send_allocated_file()



