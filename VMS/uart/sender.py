from time import sleep
from machine import Pin, UART
import machine

UART_ID = 1
BAUD = 9600

ONBOARD_LED = Pin("LED", Pin.OUT)
ONBOARD_LED.toggle()
TX_PIN = Pin(4)
RX_PIN = Pin(5)
RED_LED = Pin(15, Pin.OUT)

uart = UART(UART_ID, baudrate=BAUD, tx=TX_PIN, rx=RX_PIN)

data = 'ping'

while True:
    uart.write(data)
    ONBOARD_LED.toggle()
    sleep(1)
