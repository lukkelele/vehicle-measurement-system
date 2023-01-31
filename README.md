# Vehicle measurement system
###<pre> an embedded system that can detect and measure vehicles</pre>
Author: *Lukas Gunnarsson*<br>
Project start: *31/1-2023*<br>

---
## System
OS: *freeRTOS*
### Prerequities
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
> - Magnetic sensor (*for inductive wiring*)
> - Light seeking sensor
> - **[ INSERT MORE ]**
- Modules
> - Light dependent resistor module
> - Line tracking module
> - Small laser module (*testing*)
> - **[ INSERT MORE ]**

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

