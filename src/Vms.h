#ifndef _VMS_H
#define _VMS_H

#include "pico/stdlib.h"

/* States */
#define LOW 0
#define HIGH 1
/* Pins */
#define PIN0  1
#define PIN1  3
#define PIN2  4
#define PIN3  5
#define PIN4  6
#define PIN5  7
#define PIN6  9
#define PIN7  10
#define PIN8  11
#define PIN9  12
#define PIN10 14
#define PIN11 15
#define PIN12 16
#define PIN13 17
#define PIN14 19
#define PIN15 20
#define PIN26 31
#define PIN27 32
/* UART */
#define UART0_TX PIN0 // PIN12, PIN16
#define UART0_RX PIN1 // PIN13, PIN17
#define UART1_TX PIN4 // PIN8
#define UART1_RX PIN5 // PIN9
/* ADC */
#define ADC0 PIN26
#define ADC1 PIN27

#endif /* _VMS_H */
