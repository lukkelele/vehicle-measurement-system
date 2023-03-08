import machine
import time
import _thread

# Define the UART parameters
uart_port = machine.UART(0, baudrate=115200, bits=8, parity=None, stop=1)
uart_rx = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

# Define the function for receiving data over UART
def uart_receive():
    while True:
        if uart_port.any():
            data = uart_port.readline()
            print(data)

# Start the UART receiver thread
_thread.start_new_thread(uart_receive, ())

# Do other tasks while waiting for UART data
while True:
    print("Waiting for UART data...")
    time.sleep(1)

