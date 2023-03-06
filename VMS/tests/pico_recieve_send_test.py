# Test for the Pico W to recieve data and then to transmit it using 
# the SFTP protocol

import serial
import paramiko

ssh_conn = {
        'hostname': '192.168.1.80',
        'port': 22,
        'username': 'pi',
        }

PORT = ''
BAUD = 115200

ser = serial.Serial(PORT, BAUD)

# Set up SSH connection
passwd = input(f'{ssh_conn.username}@{ssh_conn.hostname} -> password: ')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname = ssh_conn['hostname'], 
            username = ssh_conn['username'],
            password = passwd)
