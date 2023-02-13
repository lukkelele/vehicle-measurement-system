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
#define UART_TX_PIN 8


class VMSystem
{
public:
    VMSystem();
    ~VMSystem() = default;

public:
    void initPin(uint pin, uint mode = OUT, uint val = LOW);
    void initUART();

    void setPinDir(uint pin, uint mode);
    void setPinPull(uint pin, bool up);

    uint8_t getPinValue(uint pin) const;
    uint8_t setPinValue(uint pin, uint val);

    bool transmitByte(uint8_t &byte);
    bool transmitData(const uint8_t* data, unsigned int n);

private:

    bool m_Interrupt_UART = false;
    unsigned int m_BaudRate;

};

#endif /* _VMS_H */




