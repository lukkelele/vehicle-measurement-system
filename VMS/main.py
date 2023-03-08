import picamera
import socket
import struct
import time
import io

# create a socket and bind to a port
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('wb')
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        # start a preview
        camera.start_preview()
        # give the camera time to warm up
        time.sleep(2)
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg'):
            # write the length of the capture to the stream and flush to ensure it actually gets sent
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            # rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())
            # reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
finally:
    connection.close()
    server_socket.close()
