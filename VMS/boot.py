from time import sleep
import VmsClient
import _secret as s

# Test
print('./boot.py')
client = VmsClient.VmsClient(host = s.HOST_ADDR,
                             port = s.SOCK_PORT,
                             ssid = s.WIFI_SSID,
                             password = s.WIFI_PASSWORD)

pizza_path = './img/pizza-img.jpg'
print('Testing data transfer to server')
client.send_file(pizza_path, 4096)
