from machine import Pin, UART
from time import sleep

UART_ID = 1
BAUD = 9600

ONBOARD_LED = Pin("LED", Pin.OUT)
TX_PIN = Pin(4)
RX_PIN = Pin(5)

uart = UART(UART_ID, baudrate=BAUD, tx=TX_PIN, rx=RX_PIN)

i = 0
while True:
    while uart.any() > 0:
        c = uart.read(1)
        print(c.decode('utf-8'), end='')
    sleep(0.10)
    i += 1
    if i % 60 == 0:
        print('<3')
        ONBOARD_LED.toggle()
        i = 0
