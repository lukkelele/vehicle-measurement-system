#ifndef _VMS_H
#define _VMS_H

#include "VMSPico.h"
#include "pico/stdlib.h"

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




