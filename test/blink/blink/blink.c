/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

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

void transmit(uint8_t* data, uint8_t buflen, uart_id = uart1)
{
    uart_write_blocking(UART_ID, data, buflen);
}

int main()
{
#ifdef PICO_DEFAULT_LED_PIN
    stdio_init_all();
    uart_init(UART_ID, BAUD_RATE);
    // Disable line feed conversion
    uart_set_translate_crlf(UART_ID, false);
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);

    bi_decl(bi_1pin_with_func(UART_TX_PIN, GPIO_FUNC_UART));

    while (true) 
    {
        char c = getchar();
        if (c < 128) uart_putc_raw(UART_ID, c);
        
    }

#endif
}
