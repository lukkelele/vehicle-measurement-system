/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */
#include "blink.h"

void transmit(uint8_t* data, uint8_t buflen)
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
