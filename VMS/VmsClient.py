import pico_logger as logger
from machine import UART
import _secret as secret
import wifi as _wifi
import socket
import time

# WiFi configuraton
WIFI_SSID = secret.WIFI_SSID
WIFI_PASSWORD = secret.WIFI_PASSWORD

HOST_ADDR = secret.HOST_ADDR
SOCK_PORT = secret.SOCK_PORT
DEFAULT_TIMEOUT = 15
UART_ID = 0
DEFAULT_BAUDRATE = 9600

CRLF = '\r\n'

class Error(Exception):
    pass

class VmsClient:
    
    host = HOST_ADDR
    port = SOCK_PORT
    ssid = WIFI_SSID
    password = WIFI_PASSWORD
    timeout = DEFAULT_TIMEOUT
    transmit_delay = 0.10
    wifi = _wifi.Wifi()
    sock = None
    uart = None
    uart_id = UART_ID
    baudrate = DEFAULT_BAUDRATE

    def __init__(self, host=None, port=None, ssid=None, password=None,
                       timeout=None, uart_id=None, baudrate=None):
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if ssid is not None:
            self.ssid = ssid 
        if password is not None:
            self.password = password
        # Start uart
        self.uart = self.init_uart(uart_id, baudrate)

    def _create_socket_connection(self, addr, port, timeout=None):
        try:
            sock = socket.socket()
            sock_addr = socket.getaddrinfo(addr, port)[0][-1]
            sock.connect(sock_addr)
            return sock
        except:
            raise Error("[ERROR] Could not connect to %r" % (addr))

    def connect_to_wifi(self, ssid, password):
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
            logger.log_warning("No UART id or baudrate was given, using default settings")
        logger.log_info(f'Initializing UART -> id={self.uart_id}, baudrate={self.baudrate}')
        return UART(self.uart_id, self.baudrate)

    def recieve_data(self, uart):
        data = uart.readline()
        if data is not None:
            print('recieved: %s' % data)
        return data

    def transmit_data(self, data):
        if self.sock:
            self.sock.send(data)
            time.sleep(self.transmit_delay)
        
        
    def send_log_msg(self, message):
        # Check if connection is up and running
        if self.sock and self.wifi.station is not None:
            try:
                self.sock.send(message)
            except:
                raise Error("[PICO] Could not transmit log message!")




