import _secret as s
from VMSlib import *
import logger
import socket
import time


class VMSServer:
    IMAGE_SAVE_DIR = "./img/"

    ssid = s.WIFI_SSID
    password = s.WIFI_PASSWORD
    host = s.HOST_ADDR
    port = s.SOCK_PORT
    log = logger.Logger("VMSServer")

    sock = None
    timeout = 300
    byteorder = "big"
    save_errors_threshold = 10
    save_path = IMAGE_SAVE_DIR
    chunksize = 4096

    def __init__(self, host=None, port=None, baudrate=None, chunksize=None,
                 timeout=None, byteorder=None):
        """
        Start the VMSServer.

        - host: the hostname to connect server to
        - port: the desired port for the server to operate on

        If there are no arguments passed to the constructor this will not make the
        newly created VMSServer automatically set up the socket connection.
        To start a connection, the 'connect' function has to be called manually.
        """
        self.log.info("Starting server...")
        # Setup member values
        if host is not None: self.host = host
        if port is not None: self.port = port
        if timeout is not None: self.timeout = timeout
        if baudrate is not None: self.baudrate = baudrate
        if chunksize is not None: self.chunksize = chunksize
        if byteorder is not None: self.byteorder = byteorder

        # If a host and port was passed in the constructor, try to connect
        if host and port:
            self.sock, self.conn, self.addr = self.start_connection(host=self.host, 
                                                                    port=self.port, 
                                                                    timeout=self.timeout)
        else: 
            self.log.warn(f"No host or port was provided, default settings set\nhost: {self.host}\nport: {self.port}")

    def _create_new_socket(self, host, port, timeout):
        """
        Create socket for client connection.
        Sets socket options for address reuse and binds to the host and port.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            return sock
        except:
            raise SocketConnectionError(f"Could not create socket using: {host}:{port}, timeout: {timeout}")

    def _listen(self, sock=None, port=None):
        try:
            if sock:
                self.log.info(f"Listening on {port}...")
                sock.listen()
                conn, addr = sock.accept()
                self.log.info(f"Connection established to: {addr}")
                return conn, addr
        except:
            raise SocketPortError(f"Could not start listening on {self.host}:{port}")

    def start_connection(self, host, port, timeout=20):
        """
        Setup a new socket connection
        If errors occur they will be handled inside respective function
        """
        sock = self._create_new_socket(host, port, timeout)
        conn, addr = self._listen(sock, port)
        return sock, conn, addr

    def connect(self, host, port, timeout):
        """
        Connect to the VMSClient and set member variables to be returned values.
        Also resets the 'save_errors' variable.
        """
        self.sock = self._create_new_socket(host, port, timeout)
        self.conn, self.addr = self._listen(sock=self.sock, port=port)
        self.save_errors = 0

    def _shutdown(self):
        """
        Close connections and shut down the server
        """

    def _save_file(self, filedata):
        """
        Save file locally.
        The filename is set automatically depending on available files in directory (savepath).
        """
        try:
            # If the filedata sent is not either chunk size or file size
            if len(filedata) > 0:
                timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
                file_loc = f"{self.save_path}/{timestamp}.jpg"
                with open(file_loc, 'wb') as file:
                    file.write(filedata)
                self.log.info(f"Saved: {file_loc}")
        except:
            if (self.save_errors >= self.save_errors_threshold):
                raise SaveError(f"Could not save file at {self.save_path} | File size: {len(filedata) / 1024.0} kB")
            else:
                self.save_errors += 1
                self.log.error(f"Could not save file to {self.save_path}, total save errors: {self.save_errors}")

    def _get_filesize(self, byteorder="big"):
        """ Get filesize at the start of a data transmission """
        if self.conn:
            filesize_b = self.conn.recv(4)
            filesize = int.from_bytes(filesize_b, byteorder)
            return filesize

    def on_update(self):
        """
        Update function to be run every cycle.
        Handles incoming data transmissions and other events that may occur.
        """
        if self.sock and self.conn:
            filesize = self._get_filesize()
            chunksize = self.chunksize
            # If chunk size and file size are acquired then start reading data continously
            self.log.info(f"Recieved chunksize: {chunksize}  |  filesize: {filesize}")
            if chunksize != None and filesize != None:
                    data = b""
                    self.log.info(f"Recieving file size: {filesize} and chunksize {chunksize}")
                    while len(data) < filesize:
                        recv_data = self.conn.recv(chunksize)
                        data += recv_data

                    # self.log.info(f"Data size: {len(data)}")
                    # When all data is received, save the file
                    self._save_file(data)
