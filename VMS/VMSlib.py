# -----------------------------------------------------------------------
# |                           VMS Library                               |
# -----------------------------------------------------------------------
# | Commonly shared utility amongst the VMS devices                     |
# -----------------------------------------------------------------------
# | author: Lukas Gunnarsson                                            |
# | github: https://github.com/lukkelele/vehicle-measurement-system     |
# -----------------------------------------------------------------------
#

class Error(Exception):
    pass

class SaveError(Error):
    """ Save error when writing data """
    pass

class ConnectionError(Error):
    """ Connection error """
    pass

class ConnectionTimeoutError(Error):
    """ Connection timeout error """
    pass

class SocketConnectionError(Error):
    """ Socket connection error """
    pass

class SocketPortError(Error):
    """ Socket port error, e.g failure to listen to port """
    pass

class DataTransferError(Error):
    """ Data transfer error """
    pass

class ConstructorError(Error):
    """ Constructor error """
    pass

class SerialInterfaceStartupError(Error):
    """ Serial Interface initialization error """
    pass


def DisplayDeviceConfiguration(device, host = None, port = None, baudrate = None,
                               chunksize = None, file_save_dir = None):
    """ Output the devices config in the terminal """
    print(f"""
--------- {device} ---------
> Host: {host if host != None else ""}
> Port: {port if port != None else ""}
> Baudrate: {baudrate if baudrate != None else "NULL"}
> Chunksize: {chunksize if chunksize != None else "NULL"}
> File save directory: {file_save_dir if file_save_dir != None else "NULL"}
""")

