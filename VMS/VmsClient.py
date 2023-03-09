import pico_logger as logger
from machine import UART
import _secret as s
import wifi as _wifi
import socket
import time

class VmsClient:
    DEFAULT_TIMEOUT = 15
    UART_ID = 0
    DEFAULT_BAUDRATE = 115200
    
    host = s.HOST_ADDR
    port = s.SOCK_PORT
    ssid = s.WIFI_SSID
    password = s.WIFI_PASSWORD
    timeout = DEFAULT_TIMEOUT
    transmit_delay = 0.10
    wifi = None
    sock = None
    uart = None
    uart_id = UART_ID
    baudrate = DEFAULT_BAUDRATE

    def __init__(self, host=None, port=None, ssid=None, password=None,
                       timeout=None, uart_id=None, baudrate=None):
        logger.info("Creating VMSClient")
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if ssid is not None:
            self.ssid = ssid 
        if password is not None:
            self.password = password

        # Setup wifi connection
        self.wifi = _wifi.Wifi()
        self.wifi.connect(self.ssid, self.password)
        # Setup uart communication
        self.uart = self.init_uart(uart_id, baudrate)
        # Setup socket and connect to VMSServer
        if host and port:
            self.connect(host=host, port=port)

    def _create_socket_connection(self, addr, port, timeout=None):
        logger.info("Creating new socket connection")
        try:
            sock = socket.socket()
            sock_addr = socket.getaddrinfo(addr, port)[0][-1]
            sock.connect(sock_addr)
            return sock
        except:
            print("[ERROR] Could not connect to %r" % (addr))

    def connect_to_wifi(self, ssid, password):
        if self.wifi is not None:
            self.wifi.connect(ssid, password)

    def connect(self, host=None, port=None, timeout=None):
        if host:
            self.host = host
        if port:
            self.port = port
        if timeout is None:
            timeout = self.timeout
        self.sock = self._create_socket_connection(host, port, timeout)

    def init_uart(self, uart_id=None, baudrate=None):
        if uart_id is not None:
            self.uart_id = uart_id
        if baudrate is not None:
            self.baudrate = baudrate
        if not uart_id and not baudrate:
            logger.warn("No UART id or baudrate was given, using default settings")
        logger.info(f'Initializing UART with: id={self.uart_id}, baudrate={self.baudrate}')
        return UART(self.uart_id, self.baudrate)

    def recieve_uart_data(self, chunksize=1024):
        logger.info("Recieving data")
        if self.uart and self.sock:
            file = b''
            while True:
                data = self.uart.read(chunksize)
                print(f"Recieved: {data}")
                file += data
                data_length = len(data)

                if data_length < chunksize:
                    print('len of data:', data_length)
                    break
            print(f"Returning: {file}")
            return file
            # self.send_file_bytes(file, chunksize)
                    
    def send_file(self, filepath: str, chunksize=2048):
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
        
    def send_file_bytes(self, data: bytes, chunksize=2048):
        """
        Send file to server.
        Chunksize is automatically synced on the server to whatever is set in this function
        """
        if self.sock:
            data_length = len(data)
            # Send chunk size and data length as the first 8 bytes to the server
            chunksize_bytes = chunksize.to_bytes(4, 'big')
            data_length_bytes = data_length.to_bytes(4, 'big')
            self.sock.sendall(chunksize_bytes)
            self.sock.sendall(data_length_bytes)

            # Send the data
            for i in range(0, data_length, chunksize):
                self.sock.sendall(data[i : i+chunksize])
    
    def on_update(self, chunksize=2048):
        """
        On update function, to run every cycle
        Takes care of all that the pico has to do, polling, transmission etc
        """
        sock = self.sock; uart = self.uart
        if sock and uart:
            if uart.any():
                # Read uart
                uart_data = self.recieve_uart_data(chunksize) 
                # Transmit this file in bytes to the server
                self.send_file_bytes(uart_data)

