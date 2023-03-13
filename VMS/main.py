from time import sleep
import VMSClient
import _secret as s

print('./main.py (VMSClient)')
chunksize = 1024
baudrate = 57600

client = VMSClient.VMSClient(host = s.HOST_ADDR,
                             port = s.SOCK_PORT,
                             ssid = s.WIFI_SSID,
                             password = s.WIFI_PASSWORD,
                             baudrate = baudrate)

print("Client listening on uart..")

while True:
    client.on_update(chunksize)
