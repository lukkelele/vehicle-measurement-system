/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "pico/stdlib.h"
#include "pico/stdio.h"
#define LOW 0
#define HIGH 1

#define GPIO_0 1
#define GPIO_1 3
#define GPIO_2 4
#define PIN_4  6
#define GP4 6
#define PIN_15 20

int main()
{
#ifdef PICO_DEFAULT_LED_PIN
    const uint LED_PIN = PICO_DEFAULT_LED_PIN;
    const uint TRIGGER_PIN = GPIO_0;
    const uint ECHO_PIN = GPIO_1;
    const uint STATUS_LED = GP4;

    gpio_init(LED_PIN);
    gpio_init(TRIGGER_PIN);
    gpio_init(ECHO_PIN);
    gpio_init(STATUS_LED);

    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_set_dir(TRIGGER_PIN, GPIO_OUT);
    gpio_set_dir(ECHO_PIN, GPIO_IN);
    gpio_set_dir(STATUS_LED, GPIO_OUT);

    uint echoValue;
    while (true) {
        echoValue = gpio_get(ECHO_PIN);
        while (echoValue == 0)
        {
            gpio_put(STATUS_LED, HIGH);

            gpio_put(TRIGGER_PIN, LOW);
            sleep_ms(100); // 5 us
            gpio_put(TRIGGER_PIN, HIGH);
            sleep_ms(150); // 10 us

            // gpio_put(LED_PIN, 1);
            // sleep_ms(500);
            // gpio_put(LED_PIN, 0);
            // sleep_ms(500);
            echoValue = gpio_get(ECHO_PIN);
        }
        while (echoValue == 1)
        {
            gpio_put(STATUS_LED, LOW);
            sleep_ms(1500);
            // gpio_put(STATUS_LED, LOW);
            // gpio_put(LED_PIN, HIGH);
            // sleep_ms(800);
            // gpio_put(LED_PIN, LOW);
            // sleep_ms(100);
            gpio_put(TRIGGER_PIN, LOW);
            sleep_ms(100);
            gpio_put(TRIGGER_PIN, HIGH);
            sleep_ms(150);

            echoValue = gpio_get(ECHO_PIN);
        }

    }
#endif
}
