import VmsServer

host = '127.0.0.1'
port = 65432

VmsServer.log.info("Running VmsServer test")

VmsServer.log.warning("Creating new server")
server = VmsServer.VmsServer(host, port)
VmsServer.log.info("New server created!")
