#ifndef _VMS_H
#define _VMS_H

#include <stdio.h>
#include <math.h>

#include "VMSPico.h"
#include "pico/stdlib.h"
#include "hardware/gpio.h"

// #include "pico/stdio.h"
#include "pico/binary_info.h"
#include "hardware/uart.h"

#define UART_ID uart1
#define BAUD_RATE 9600
#define UART_TX_PIN 8
/* 
 *  Storage: 2MB
 *  TODO: Fix 'debug' and 'release' configs to optimize code
 */

class VMSystem
{
private:
    void initPin(uint pin, uint mode = OUT, val = LOW);

    void setPinDir(uint pin, uint mode);
    void setPinPull(uint pin, bool up);

    uint8_t getPinValue(uint pin);
    uint8_t setPinValue(uint pin, uint val);

    bool transmitData(uint8_t byte, 

};

#endif /* _VMS_H */




