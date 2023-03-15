import VMSServer
import _secret as s

HOST = s.HOST_ADDR
PORT = s.SOCK_PORT
BAUDRATE = 115200
CHUNKSIZE = 4096

vmsServer = VMSServer.VMSServer(host = HOST,
                                port = PORT,
                                baudrate = BAUDRATE,
                                chunksize = CHUNKSIZE
                                )

while True:
    vmsServer.on_update()

print("Exiting...")
