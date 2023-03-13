import VMSServer

host = '127.0.0.1'
port = 65432

VMSServer.log.info("Running VMSServer test")
VMSServer.log.info("Creating new server")

server = VMSServer.VMSServer(host, port)

VMSServer.log.info("New server created!")
