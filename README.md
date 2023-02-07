# Vehicle measurement system
an embedded system that can detect and measure vehicles

---
Author: *Lukas Gunnarsson*<br>
Project start: *24/1-2023*<br>

---
## System
OS: *freeRTOS*
### Prerequities
- gcc
- git
- freeRTOS
- CMake


#### Components
- Raspberry Pi Pico
- Breadboard
- Wiring
- LEDs
- Sensors 
> - PIR sensor
> - Ultrasonic sensor
> - Magnetic sensor (*for inductive wiring*)
> - Light seeking sensor
> - Light dependent resistor
> - Line tracking module
> - Small laser module (*testing*)
> - **...**

---
## Configuration
#### Submodules

> <pre>git clone https://github.com/RaspberryPi/pico-sdk --recurse-submodules
> git clone -b smp https://github.com/FreeRTOS/FreeRTOS-Kernel --recurse-submodules</pre>

##### Environment variables

> <pre>export PICO_SDK_PATH=$PWD/pico-sdk
> export FREERTOS_KERNEL_PATH=$PWD/FreeRTOS-Kernel</pre>

---

## Building

