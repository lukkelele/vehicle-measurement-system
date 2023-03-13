from time import sleep
import network
import binascii

class Wifi:
    
    ssid = None
    password = None
    timeout = 10

    def __init__(self, ssid=None, password=None, timeout=None):
        if ssid is not None:
            self.ssid = ssid
        if password is not None:
            self.password = password
        if timeout is None:
            timeout = self.timeout

    def connect(self, ssid, passwd, timeout = 15):
        print('Connecting to WiFi: %s ' % ssid, end='')
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(ssid, passwd)
        is_timeout = False
        i = 0

        while not station.isconnected():
            print('.', end='')
            i += 1
            sleep(1)
            if i > timeout:
                print(' connection couldn\'t be established')
                station.active(False)
                is_timeout = True
        print()
        if not is_timeout:
            return station
        
        return None
       
    def scan(self):
        if (self.station is not None):
            print('Starting scan...')
            try:
                scan = self.station.scan()
                sleep(1.5)
                for n in scan:
                    network_name = n[0].decode('UTF-8')
                    network_address = binascii.hexlify(n[1]).decode('UTF-8')
                    network_channel = n[2]
                    print('''Network
                          name: %s
                          address: %s
                          channel: %s
                          ''' % (network_name, network_address, network_channel))
            except:
                print('Error scanning networks')
        else:
            print('Scanning could not start!\nMake sure the connection has been established')

    def isConnected(self, station):
        return station != None 

