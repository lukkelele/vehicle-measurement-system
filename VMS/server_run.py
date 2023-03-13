import VMSServer
import _secret as s

HOST = s.HOST_ADDR
PORT = s.SOCK_PORT
BAUDRATE = s.default.BAUDRATE
CHUNKSIZE = s.default.CHUNKSIZE
TIMEOUT = s.default.TIMEOUT

print("Starting VMSServer...")
vmsServer = VMSServer.VMSServer(host = HOST,
                                port = PORT,
                                timeout = TIMEOUT,
                                baudrate = BAUDRATE,
                                chunk_size = CHUNKSIZE
                                )



