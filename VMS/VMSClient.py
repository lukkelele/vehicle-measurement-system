from machine import UART, Pin
# import default_config as default
import pico_logger as logger
import _secret as s
import wifi as _wifi
import socket
import time

UART_ID = 0
BAUDRATE = 115200
CHUNKSIZE = 4096
TIMEOUT = 10

class VMSClient:
    ONBOARD_LED = Pin("LED", Pin.OUT)
    tx_pin = Pin(0)
    rx_pin = Pin(1)

    host = s.HOST_ADDR
    port = s.SOCK_PORT
    ssid = s.WIFI_SSID
    password = s.WIFI_PASSWORD
    wifi = None
    sock = None
    uart = None
    uart_id = UART_ID
    baudrate = BAUDRATE
    timeout = TIMEOUT

    def __init__(self, host=None, port=None, ssid=None, password=None,
                       timeout=None, uart_id=None, baudrate=None):
        # logger.info("Creating VMSClient")
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if ssid is not None:
            self.ssid = ssid 
        if password is not None:
            self.password = password
        if timeout is not None:
            self.timeout = timeout

        self.ONBOARD_LED.value(1)
        time.sleep(1.5)

        # Setup wifi connection
        self.wifi = _wifi.Wifi()
        self.wifi.connect(self.ssid, self.password)

        # Setup uart communication
        self.uart = self.init_uart(uart_id, baudrate)

        # Setup socket and connect to VMSServer
        if host and port:
            self.connect(host=self.host, port=self.port, timeout=self.timeout)

    def _create_socket_connection(self, addr, port, timeout):
        # logger.info("Creating new socket connection")
        try:
            sock = socket.socket()
            # sock.settimeout(timeout)
            sock_addr = socket.getaddrinfo(addr, port)[0][-1]
            sock.connect(sock_addr)
            return sock
        except:
            print("[ERROR] Could not connect to %r" % (addr))

    def connect_to_wifi(self, ssid, password):
        if self.wifi is not None:
            self.wifi.connect(ssid, password)

    def connect(self, host, port, timeout):
        self.sock = self._create_socket_connection(host, port, timeout)

    def init_uart(self, uart_id=None, baudrate=None):
        if uart_id is not None:
            self.uart_id = uart_id
        if baudrate is not None:
            self.baudrate = baudrate
        if not uart_id and not baudrate:
            logger.warn("No UART id or baudrate was given, using default settings")
        # logger.info(f'Initializing UART with: id={self.uart_id}, baudrate={self.baudrate}')
        return UART(self.uart_id, self.baudrate, parity=None, stop=1, bits=8, tx=self.tx_pin, rx=self.rx_pin)

    def recieve_uart_data(self, chunksize = CHUNKSIZE):
        """ Saves all data to the onboard memory and returns the file in bytes """
        if self.uart:
            file = b""
            filesize = int.from_bytes(self.uart.read(4))
            datasize = 0
            # while True:
            while filesize > datasize:
                data = self.uart.read(chunksize)
                datasize = len(data)
                file += data
                # if datasize < chunksize: break

            return file

    def recieve_and_send_uart_data(self, chunksize = CHUNKSIZE):
        """ Recieves data on the UART and sends it directly to the server """
        if self.uart and self.sock:
            # data_size = int.from_bytes(self.uart.read(4))
            data_size = self.uart.read(4) # is in bytes already
            # print("Data size: ", data_size)
            chunksize_bytes = chunksize.to_bytes(4, 'big')
            self.sock.sendall(chunksize_bytes)
            self.sock.sendall(data_size)

            # FIXME: Returns none
            while True:
                data = self.uart.read(chunksize)
                print(data)
                # print(f"Recieved: {data}")
                self.sock.sendall(data)

                data_len = len(data)
                if data_len < chunksize:
                    break

    def send_file(self, filepath: str, chunksize = CHUNKSIZE):
        """
        Send file to server.
        Chunksize is automatically synced on the server to whatever is set in this function
        """
        if self.sock:
            with open(filepath, 'rb') as file:
                data = file.read()
                data_length = len(data)
                # Send chunk size and data length as the first 8 bytes to the server
                chunksize_bytes = chunksize.to_bytes(4, 'big')
                data_length_bytes = data_length.to_bytes(4, 'big')
                self.sock.sendall(chunksize_bytes)
                self.sock.sendall(data_length_bytes)

                # Send the data
                for i in range(0, data_length, chunksize):
                    self.sock.sendall(data[i : i+chunksize])
        
    def send_file_bytes(self, data: bytes, chunksize = CHUNKSIZE):
        """
        Send file to server.
        Chunksize is automatically synced on the server to whatever is set in this function
        """
        if self.sock:
            data_length = len(data)
            print("DATA LENGTH: ", data_length)
            # Send chunk size and data length as the first 8 bytes to the server
            chunksize_bytes = chunksize.to_bytes(4, "big")
            data_length_bytes = data_length.to_bytes(4, "big")
            self.sock.sendall(chunksize_bytes)
            self.sock.sendall(data_length_bytes)

            # Send the data
            for i in range(0, data_length, chunksize):
                self.sock.sendall(data[i : i+chunksize])
    
    def send_allocated_file(self, chunksize = CHUNKSIZE):
        """ 
        Send a file using allocated memory instead of sending the file in a stream-like manner. 
        """
        self.ONBOARD_LED.value(1)
        uart_data = self.recieve_uart_data(chunksize) 
        self.send_file_bytes(uart_data, chunksize=chunksize)

    def send_file_stream(self, chunksize = CHUNKSIZE):
        """
        Send a file using a continous stream of data
        """
        self.ONBOARD_LED.value(1)
        uart_data = self.recieve_uart_data(chunksize) 
        self.send_file_bytes(uart_data, chunksize=chunksize)

    def on_update(self, chunksize = CHUNKSIZE):
        """
        On update function, to run every cycle
        Takes care of all that the pico has to do, polling, transmission etc
        """
        self.ONBOARD_LED.value(0)
        if self.sock and self.uart:
            if self.uart.any():
                self.send_allocated_file(chunksize=chunksize)
                # FIXME
                # self.recieve_and_send_uart_data(chunksize=chunksize) 
