#ifndef _VMS_H
#define _VMS_H

#include "VMSPico.h"
#include <stdio.h>
#include <math.h>

#include "pico/stdlib.h"
#include "pico/stdio.h"
#include "pico/binary_info.h"
#include "hardware/uart.h"
#include "hardware/gpio.h"

#define UART_ID uart1
#define BAUD_RATE 9600
// #define UART_IRQ_ENABLED 1

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

    bool transmitByte(uint8_t &byte);
    bool transmitData(const uint8_t* data, unsigned int n);

    // TODO: Don't know the importance of using interrupts right now
    // Static for callbacks
    static void UART_RX_HANDLER() { NULL; }

private:

    unsigned int m_BaudRate;

};

#endif /* _VMS_H */




