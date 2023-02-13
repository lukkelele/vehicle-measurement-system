#ifndef _VMSPICO_H
#define _VMSPICO_H
#include "hardware/irq.h"
#include "hardware/uart.h"
#include "hardware/gpio.h"

#ifndef _u
#ifdef __ASSEMBLER__
#define _u(x) x
#else
#define _u(x) x ## u
#endif
#endif

#define UART0_BASE _u(0x40034000)
#define UART1_BASE _u(0x40038000)

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

#define UART_TX_PIN 0
#define UART_RX_PIN 1

#define BYTE 8
#define PAYLOAD_FORMAT BYTE
#define STOP_BITS 1
#define PARITY UART_PARITY_NONE

/* ADC */
#define ADC0 GP26
#define ADC1 GP27

#endif /* _VMSPICO_H */
