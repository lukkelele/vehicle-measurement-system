import default_config as default
import _secret as secret
from logger import log
import socket
import time


class Error(Exception):
    pass

class SaveError(Error):
    """ Save error when writing data """
    pass

class ConnectionError(Error):
    """ Connection error """
    pass


class VMSServer:


    ssid = secret.WIFI_SSID
    password = secret.WIFI_PASSWORD
    host = secret.HOST_ADDR
    port = secret.SOCK_PORT
    
    sock = None
    timeout = default.TIMEOUT
    save_errors_threshold = default.FAILED_SAVE_THRESHOLD
    save_path = default.SAVE_DIR

    def __init__(self, host=None, port=None, baudrate=None, chunk_size=None, timeout=None):         
        """
        Start the VMSServer.
        
        - host: the hostname to connect server to
        - port: the desired port for the server to operate on

        If there are no arguments passed to the constructor this will not make the 
        newly created VMSServer automatically set up the socket connection.
        To start a connection, the 'connect' function has to be called manually.
        """
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if baudrate is not None:
            self.baudrate = baudrate
        if chunk_size is not None:
            self.chunk_size = chunk_size
        if timeout is not None:
            self.timeout = timeout

        if host and port:
            self.connect(host=host, port=port, timeout=self.timeout)
        else:
            log.warn(f"No host or port was provided, default settings set\nhost: {self.host}\nport: {self.port}")

    def _create_socket(self, host, port, timeout):
        """ 
        Create socket for client connection.
        Sets socket options for address reuse and binds to the host and port.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return sock
        except:
            raise ConnectionError(f"Could not create socket using: {host}:{port}, timeout: {timeout}")

    def _listen(self):
        try:
            if self.sock:
                log.info(f"Listening on {self.port}...")
                self.sock.listen()
                conn, addr = self.sock.accept()
                return conn, addr
        except:
            raise Error(f"Could not start listening on {self.host}:{self.port}")

    def connect(self, host, port, timeout):
        """ 
        Connect to the VMSClient and set member variables to be returned values.
        Also resets the 'save_errors' variable.
        """
        self.sock = self._create_socket(host, port, timeout)
        self.conn, self.addr = self.sock._listen()
        self.save_errors = 0

    def _shutdown(self):
        """
        Close connections and shut down the server
        """

    def recieve_data(self, uart):
        data = uart.readline()
        if data is not None:
            log.info('recieved: %s' % data)
        return data

    def transmit_data(self, data):
        if self.sock:
            self.sock.send(data)

    def _save_file(self, filedata):
        """ 
        Save file locally.
        The filename is set automatically depending on available files in directory (savepath).
        """
        try:
            filename = 'img.jpg'
            file_loc = f"{self.savepath}/{filename}"
            with open(file_loc, 'wb') as file:
                file.write(filedata)
        except:
            if (self.save_errors >= self.save_errors_threshold):
                raise SaveError(f"Could not save file at {self.savepath} | File size: {len(filedata) / 1024.0} kB")
            else:
                self.save_errors += 1
                log.error(f"Could not save file to {self.savepath}, total save errors: {self.save_errors}")

    def _get_size(self, byteorder="big"):
        """ 
        Get chunk and file sizes at the beginning of data transmissions.
        Reads first 4 bytes and converts them to an actual number.

        - byteorder: big or little, endian order
        - returns: the number of the 4 read bytes if connection is up, else None
        """
        if self.conn:
            size_b = self.conn.recv(4)
            size = int.from_bytes(size_b, byteorder=byteorder)
            return size
        return None

    def on_update(self):
        """ 
        Update function to be run every cycle.
        Handles incoming data transmissions and other events that may occur.
        """
        if self.sock and self.conn:
            chunk_size = self._get_size()
            filesize = self._get_size()
            # If chunk size and file size are acquired then start reading data continously
            if chunk_size and filesize:
                    data = b""
                    while len(data) < filesize:
                        recv_data = self.conn.recv(chunk_size) 
                        data += recv_data
                        log.info(f"Current data size: {len(data)}")
                        log.info(f"Actual file size: {filesize}")

                    # When all data is recieved, save the file
                    self._save_file(data)
                

