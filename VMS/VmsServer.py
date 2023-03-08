from logger import log
import socket
import time
import _secret as secret

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

class VmsServer:
    
    host = HOST_ADDR
    port = SOCK_PORT
    ssid = WIFI_SSID
    password = WIFI_PASSWORD
    timeout = DEFAULT_TIMEOUT
    transmit_delay = 0.10
    sock = None

    def __init__(self, host=None, port=None):         
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port

        self._bind_socket()
        self._listen()

    def _bind_socket(self):
        log.warn("Binding to socket")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _listen(self):
        try:
            if self.sock:
                log.debug(f"Listening on {self.port}...")
                self.sock.listen()
                conn, addr = self.sock.accept()
                return conn, addr
        except:
            raise Error("_listen failed to start")

    def recieve_data(self, uart):
        data = uart.readline()
        if data is not None:
            log.info('recieved: %s' % data)
        return data

    def transmit_data(self, data):
        log.info(f"Transmitting -> {data}")
        if self.sock:
            self.sock.send(data)
            time.sleep(self.transmit_delay)
