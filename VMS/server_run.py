import VMSServer
import _secret as s

HOST = s.HOST_ADDR
PORT = s.SOCK_PORT
BAUDRATE = 57600
CHUNKSIZE = 2048

vmsServer = VMSServer.VMSServer(host = HOST,
                                port = PORT,
                                baudrate = BAUDRATE,
                                chunk_size = CHUNKSIZE
                                )

while True:
    vmsServer.on_update()

print("Exiting...")
