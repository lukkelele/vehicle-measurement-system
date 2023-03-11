from time import sleep
import VmsClient
import _secret as s

print('./main.py')
chunksize = 1024
baudrate = 57600

client = VmsClient.VmsClient(host = s.HOST_ADDR,
                             port = s.SOCK_PORT,
                             ssid = s.WIFI_SSID,
                             password = s.WIFI_PASSWORD,
                             baudrate = baudrate)

print("Client listening on uart..")
while True:
    #client.recieve_and_send_uart_data(chunksize)
    client.on_update(chunksize)
    # client.test_uart_recieval()
    # sleep(0.25)
