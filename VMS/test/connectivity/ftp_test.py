from ftplib import FTP

print('Starting FTP test')

ftp = FTP('ftp.dlptest.com', user='dlpuser', passwd='rNrKYTX9g7z3RgJRmxWuGHbeu')
ftp_pwd = ftp.pwd()
ftp.retrlines('LIST')

print('Exiting FTP test')
