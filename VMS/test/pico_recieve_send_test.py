# Test for the Pico W to recieve data and then to transmit it using 
# the SFTP protocol

import _secret as secret
import serial
import paramiko

ssh_conn = {
        'hostname': secret.PI_HOSTNAME,
        'port': secret.PI_PORT,
        'username': secret.PI_USERNAME,
        'password': secret.PI_PASSWORD
        }

PORT = ''
BAUD = 115200

ser = serial.Serial(PORT, BAUD)

# Set up SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname = ssh_conn['hostname'], 
            username = ssh_conn['username'],
            password = ssh_conn['password'])
