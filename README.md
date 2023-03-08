# Vehicle measurement system
an embedded system that can detect and measure vehicles

---
Author: *Lukas Gunnarsson*<br>
Project start: *24/1-2023*<br>

---
## System
OS: *freeRTOS*
### Dependencies
- freeRTOS
- paramiko 
- picamera


#### Components
- Raspberry Pi Pico
- Breadboard
- Wiring
- LEDs
- Sensors 


---

## Building


## Pico

UART communication via GP4 and GP5 (physical pin 6 and 7)  
<br>

| Resolution | FPS | Depth (bits) | Frame size (mb)| Data transfer/s (mb/s) |
|----------  | --- | --- | --- | --- |
| 640x480    | 20  |   24    | 0.920 | 18.4 |
| 640x480    | 20  |   12    | 0.461 | 9.22 |
| 1280x1080 | 20 | 24 | 4.147 | 82.94 |
| 1280x1080 | 20 | 12 | 2.074 | 41.48 |
