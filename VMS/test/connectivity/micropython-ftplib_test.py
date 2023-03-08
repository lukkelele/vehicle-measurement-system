from ftplib import FTP
import _secret as secret

ftp = FTP(host=secret.FTP_CONFIG.hostname, user=secret.FTP_CONFIG.username, passwd=secret.FTP_CONFIG.password)
print(ftp.debug(3))
ftp_pwd = ftp.pwd()
ftp.retrlines('LIST')
print('Exiting FTP test')
