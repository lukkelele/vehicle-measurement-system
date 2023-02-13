#pragma once

#include <stdio.h>
#include <math.h>
#include "pico/stdlib.h"
// #include "pico/stdio.h"
#include "pico/binary_info.h"
#include "hardware/uart.h"

#define UART_ID uart1
#define BAUD_RATE 9600
#define UART_TX_PIN 8

#define LOW 0
#define HIGH 1

#define GPIO_0 1
#define GPIO_1 3
#define GPIO_2 4
#define PIN_4  6
#define GP4 6
#define PIN_15 20

// minicom -b 115200 -o -D /dev/serial0
