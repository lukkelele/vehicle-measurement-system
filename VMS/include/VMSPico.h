#pragma once

#if defined(PICO_DEFAULT_LED_PIN)
    #define ONBOARD_LED PICO_DEFAULT_LED_PIN
#else
    #define ONBOARD_LED 25
#endif

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
#define GP0  0
#define GP1  1
#define GP2  2
#define GP3  3
#define GP4  4
#define GP5  5
#define GP6  6
#define GP7  7
#define GP8  8
#define GP9  9
#define GP10 10
#define GP11 11
#define GP12 12
#define GP13 13
#define GP14 14
#define GP15 15
#define GP22 22
#define GP26 26
#define GP27 27

/* UART */
#define UART_TX_PIN 0
#define UART_RX_PIN 1


