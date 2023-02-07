/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "pico/stdlib.h"
#define LOW 0
#define HIGH 1

#define GPIO_0 1
#define GPIO_1 3
#define GPIO_2 4

int main() {
#ifndef PICO_DEFAULT_LED_PIN
// #warning blink example requires a board with a regular LED
#else
    const uint LED_PIN = PICO_DEFAULT_LED_PIN;
    const uint TRIGGER_PIN = GPIO_0;
    const uint ECHO_PIN = GPIO_1;
    const uint GPIO_2 = 4;
    gpio_init(LED_PIN);
    gpio_init(TRIGGER_PIN);
    gpio_init(ECHO_PIN);

    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_set_dir(TRIGGER_PIN, GPIO_OUT);
    gpio_set_dir(ECHO_PIN, GPIO_IN);
    while (true) {
        gpio_put(TRIGGER_PIN, LOW)
        sleep_us(2);

        gpio_put(TRIGGER_PIN, HIGH)
        sleep_us(5);
        uint echoValue = gpio_get(ECHO_PIN);
        while (echoValue == 0);

        // gpio_put(LED_PIN, 1);
        // sleep_ms(2000);
        // gpio_put(LED_PIN, 0);
        // sleep_ms(500);
    }
#endif
}
