#pragma once


#include <stdio.h>
#include <stdint.h>
#include <math.h>

#include "pico/stdlib.h"
#include "pico/stdio.h"
#include "pico/binary_info.h"

#include "hardware/irq.h"
#include "hardware/uart.h"
#include "hardware/gpio.h"

#include "VMSPico.h"

#define BYTE 8
#define PAYLOAD_FORMAT BYTE
#define STOP_BITS 1
#define PARITY UART_PARITY_NONE
#define UART_ID uart1
#define BAUD_RATE 9600

#define LOG(x) printf("%s\n", x)

class VMSystem
{
public:
    VMSystem(bool enableUART = false);
    ~VMSystem() = default;

public:
    void initPin(uint pin, uint direction = OUT, uint val = LOW);
    void initUART();

    void setPinDir(uint pin, uint direction) { gpio_set_dir(pin, direction); }
    void setPinPull(uint pin, bool up);

    void setPinValue(uint pin, uint val) { gpio_put(pin, val); }
    uint8_t getPinValue(uint pin) const { return gpio_get(pin); }

    void togglePin(uint pin);

    bool transmitByte(uint8_t &byte);
    bool transmitData(const uint8_t* data, unsigned int n);

    // TODO: Don't know the importance of using interrupts right now
    // Static for callbacks
    static void UART_RX_HANDLER() { NULL; }

private:
    unsigned int m_BaudRate;

};





