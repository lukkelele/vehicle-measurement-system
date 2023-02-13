#ifndef _VMSPICO_H
#define _VMSPICO_H

/* Directions */
#define IN  0
#define OUT 1
/* States */
#define LOW  0
#define HIGH 1
/* Inverted states */
#define invLOW  1
#define invHIGH 0
/* General output/input pins */
#define GP0  1
#define GP1  3
#define GP2  4
#define GP3  5
#define GP4  6
#define GP5  7
#define GP6  9
#define GP7  10
#define GP8  11
#define GP9  12
#define GP10 14
#define GP11 15
#define GP12 16
#define GP13 17
#define GP14 19
#define GP15 20
#define GP26 31
#define GP27 32
/* UART */
#define UART0_TX GP0 // GP12, GP16
#define UART0_RX GP1 // GP13, GP17
#define UART1_TX GP4 // GP8
#define UART1_RX GP5 // GP9
/* ADC */
#define ADC0 GP26
#define ADC1 GP27

#endif /* _VMSPICO_H */

/*
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
*/

