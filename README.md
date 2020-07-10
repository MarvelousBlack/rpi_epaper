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

#### GDEW042T2 (http://www.e-paper-display.cn/products_detail/productId=333.html)
Support BW mode , 4gray mode and partial reflash. I guess it also support waveshare 4.2inch_e-Paper HAT(Not tested).

## Usage(Here using epd2in7 for example)
This library uses GPIO, so you must have permission to access them.  
### Initialize the e-paper hardware: 
```
from libepd import epd2in7
epd = epd2in7.EPD()
epd.init()
```
### Clear Screen
It will reflash full screen to white or black. (Default is 0xFF white) 
```
epd.clear(0xFF)
```
### Display frame
Just call `epd.display_frame(img,mode)`  
mode can be `BW,GRAY,PARTIAL,FAST`.(Default is BW)  
```
BW -> black and white
GRAY -> 4 levels of gray
PARTIAL > same as BW, but no flash.
```
BW and GRAY will flush and reflash screen within a few cycles -  inverse image, black, white, black again. That can reduces burn-in and ghosting.
Note using fast mode may make your e-paper display permanently unrecoverable damage.  
example:
```
Himage = Image.new('L', (epd.height, epd.width), 255)
epd.display_frame(Himage,epd2in7.BW)
```
### Partial display frame
Different from the previous, this function will only reflash the screen in a specific area, rather than full screen. The area size will depending on your give image.   
This function have it's limit, see the specific file for details.
```
partial_display_frame(img,x_start,y_start,mode=PARTIAL)
```
example:
```
image_2 = Image.new('L', (60,60), 0)
epd.partial_display_frame(image_2,0,0)
```

### Sleep mode
According to wiki, if you needn't refresh the e-paper but need to power on your development board or Raspberry Pi for long time, you neet set e-paper to sleep mode. Otherwise, the voltage of panel keeps high and it will damage the panel.
```
epd.sleep()
```
If you want to use `module_exit`, you can 
```
from libepd import epdconfig
epdconfig.module_exit()
```

