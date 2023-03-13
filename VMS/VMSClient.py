from machine import UART, Pin
import default_config as default
import pico_logger as logger
import _secret as s
import wifi as _wifi
import socket
import time

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
    uart_id = default.UART_ID
    baudrate = default.BAUDRATE
    timeout = default.TIMEOUT

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
            sock.settimeout(timeout)
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

    def recieve_uart_data(self, chunk_size=1024):
        """ Saves all data to the onboard memory and returns the file in bytes """
        if self.uart:
            file = b""
            while True:
                data = self.uart.read(chunk_size)
                # print(f"Recieved: {data}")
                data_len = len(data)
                file += data
                if data_len < chunk_size:
                    break

            # print(f"Returning: {file}")
            return file

    def recieve_and_send_uart_data(self, chunk_size=1024):
        """ Recieves data on the UART and sends it directly to the server """
        if self.uart and self.sock:
            # data_size = int.from_bytes(self.uart.read(4))
            data_size = self.uart.read(4) # is in bytes already
            # print("Data size: ", data_size)
            chunk_size_bytes = chunk_size.to_bytes(4, 'big')
            self.sock.sendall(chunk_size_bytes)
            self.sock.sendall(data_size)

            # FIXME: Returns none
            while True:
                data = self.uart.read(chunk_size)
                print(data)
                # print(f"Recieved: {data}")
                self.sock.sendall(data)

                data_len = len(data)
                if data_len < chunk_size:
                    break

    def send_file(self, filepath: str, chunk_size=1024):
        """
        Send file to server.
        Chunksize is automatically synced on the server to whatever is set in this function
        """
        if self.sock:
            with open(filepath, 'rb') as file:
                data = file.read()
                data_length = len(data)
                # Send chunk size and data length as the first 8 bytes to the server
                chunk_size_bytes = chunk_size.to_bytes(4, 'big')
                data_length_bytes = data_length.to_bytes(4, 'big')
                self.sock.sendall(chunk_size_bytes)
                self.sock.sendall(data_length_bytes)

                # Send the data
                for i in range(0, data_length, chunk_size):
                    self.sock.sendall(data[i : i+chunk_size])
        
    def send_file_bytes(self, data: bytes, chunk_size=1024):
        """
        Send file to server.
        Chunksize is automatically synced on the server to whatever is set in this function
        """
        if self.sock:
            data_length = len(data)
            # Send chunk size and data length as the first 8 bytes to the server
            chunk_size_bytes = chunk_size.to_bytes(4, "big")
            data_length_bytes = data_length.to_bytes(4, "big")
            self.sock.sendall(chunk_size_bytes)
            self.sock.sendall(data_length_bytes)

            # Send the data
            for i in range(0, data_length, chunk_size):
                self.sock.sendall(data[i : i+chunk_size])
    
    def send_allocated_file(self, chunk_size=1024):
        """ 
        Send a file using allocated memory instead of sending the file in a stream-like manner. 
        """
        self.ONBOARD_LED.value(1)
        uart_data = self.recieve_uart_data(chunk_size) 
        self.send_file_bytes(uart_data)

    def send_file_stream(self, chunk_size=1024):
        """
        Send a file using a continous stream of data
        """
        self.ONBOARD_LED.value(1)
        uart_data = self.recieve_uart_data(chunk_size) 
        self.send_file_bytes(uart_data)

    def on_update(self, chunk_size=1024):
        """
        On update function, to run every cycle
        Takes care of all that the pico has to do, polling, transmission etc
        """
        self.ONBOARD_LED.value(0)
        if self.sock and self.uart:
            if self.uart.any():
                # self.send_allocated_file(chunk_size=chunk_size)
                # FIXME
                self.recieve_and_send_uart_data(chunk_size=chunk_size) 
