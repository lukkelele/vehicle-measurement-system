import os
import paramiko
import datetime

pico_conn = {
        'hostname': '',
        'port': 22,
        'username': 'picow',
        }

# Set up SSH connection to Pico W
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

passwd = input(f'{pico_conn.username}@{pico_conn.hostname} -> password: ')
ssh.connect(hostname = pico_conn['hostname'],
            username = pico_conn['username'],
            password = passwd,
            port = pico_conn['port'])

# Open an SFTP session
sftp = ssh.open_sftp()

# Set up local directory to store received data
local_dir = './local_test_dir' 
if not os.path.exists(local_dir):
    os.makedirs(local_dir)

# Receive data from Pico W and store it locally in timestamped order
while True:
    # Wait for data from Pico W
    file_name = sftp.recv(1024).decode()

    # Check if the received data is the end signal
    if file_name == 'end':
        break

    # Create a timestamped file name for the received data
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d-%H-%M-%S')
    local_file_name = f"{timestamp}_{file_name}"

    # Store the received data locally
    local_file_path = os.path.join(local_dir, local_file_name)
    with open(local_file_path, 'wb') as f:
        sftp.getfo(file_name, f)


sftp.close()
ssh.close()
