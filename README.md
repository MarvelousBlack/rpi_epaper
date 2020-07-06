# rpi_epaper
A python library to easy draw on Waveshare e-Paper HAT on Raspberry Pi.

## Depends:
- python-pillow
- RPi.GPIO
- spidev

## Pin
 |E-Paper Screen | Raspberry Pi |
 |:-:|:-:|
 | VCC | 3.3 |
 | GND | GND |
 | DIN | MOSI |
 | CLK | SCLK |
 | CS | 24 (Physical, BCM: CE0, 8) |
 | D/C | 22 (Physical, BCM: 25) |
 | RES | 11 (Physical, BCM: 17) |
 | BUSY| 18 (Physical, BCM: 24) |

## Supported epaper
#### waveshare 2.7inch_e-Paper (http://www.waveshare.net/wiki/2.7inch_e-Paper_HAT)
Support BW mode , 4gray mode and partial reflash.
