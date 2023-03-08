import _secret as secret
from time import sleep
from machine import Pin, reset
from ftplib import FTP
import network
import urequests
import socket
import binascii

ONBOARD_LED = Pin("LED", Pin.OUT)
ssid = secret.WIFI_SSID
passwd = secret.WIFI_PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

pico_ip = wlan.ifconfig()[0]
print(pico_ip)

scan = wlan.scan()
sleep(1)
for n in scan:
    network_name = n[0].decode('UTF-8')
    network_address = binascii.hexlify(n[1]).decode('UTF-8')
    network_channel = n[2]
    print('''Network
          name: %s
          address: %s
          channel: %s
          ''' % (network_name, network_address, network_channel))

print(scan)


print('Connecting to WiFi: %s ' % ssid, end='')
wlan.connect(ssid, passwd)

i = 0
while not wlan.isconnected():
    print('.', end='')
    i += 1
    ONBOARD_LED.toggle()
    sleep(1)
    if i > 60:
        print(' connection couldn\'t be established')
        break

if wlan.isconnected():
    print('\nStarting FTP connection')
    ftp = FTP(host=secret.FTP_CONFIG.hostname, user=secret.FTP_CONFIG.username, passwd=secret.FTP_CONFIG.password)
    ftp_pwd = ftp.pwd()
    ftp.retrlines('LIST')
    print('Exiting FTP test')
    #query_url = 'https://www.google.com'
    #print('1. Querying -> %s' % query_url)
    #r = urequests.get(query_url)
    #sleep(5)
    #print(r.content)
    #r.close()
