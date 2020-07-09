"""epd2in7 - e-paper display library for the Waveshare 2.7inch e-Paper HAT """
# Copyright (C) 2020 megumifox <i@megumifox.com>


import logging
from . import epdconfig
from .lut_2in7 import BW_LUT,GrayLUT,Partial_LUT,Fast_LUT
from PIL import Image
from math import floor, ceil


logger = logging.getLogger('epd2in7')

# Display resolution
EPD_WIDTH       = 176
EPD_HEIGHT      = 264

GRAY1  = 0xff #white
GRAY2  = 0x80
GRAY3  = 0x40 #gray
GRAY4  = 0x00 #Blackest

BW = 0x00
GRAY = 0x01
PARTIAL = 0x02
FAST = 0x03

def _nearest_integer_of_8(num,round_up=False):
    if round_up:
        return ceil(num/8)*8
    else:
        return floor(num/8)*8

def _pil1bit(image8Bit,threshold = 80):
    # PIL's Image.convert function performs dithering by default, when convert the image to 1-bit.
    # But this in the low resolution screen will make things worse, so here use point to convert image.
    # https://computergraphics.stackexchange.com/questions/5934/algorithms-to-anti-alias-or-somehow-improve-binary-1-bit-drawings-and-fonts/5940#5940
    image1Bit = image8Bit.point(lambda x: 0 if x < threshold else 0xFF, mode='L')
    return image1Bit

class EPD:
    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.GRAY1  = GRAY1 # white
        self.GRAY2  = GRAY2
        self.GRAY3  = GRAY3 # gray
        self.GRAY4  = GRAY4 # Blackest
        self.last_frame = Image.new('L', (self.width, self.height), 255)
        
    def _set_lut(self,mode):
        if mode == BW:
            lut = BW_LUT
        elif mode == GRAY:
            lut = GrayLUT
        elif mode == PARTIAL:
            lut = Partial_LUT
        elif mode == FAST:
            lut = Fast_LUT
        else:
            raise ValueError('invalid mode')

        epdconfig.send_command(0x20) # vcom
        for byte in lut.lut_vcom_dc:
            epdconfig.send_data(byte)

        epdconfig.send_command(0x21) # ww -- #red not use
        for byte in lut.lut_ww:
            epdconfig.send_data(byte)

        epdconfig.send_command(0x22) # bw r
        for byte in lut.lut_bw:
            epdconfig.send_data(byte)

        epdconfig.send_command(0x23) # wb w
        for byte in lut.lut_wb:
            epdconfig.send_data(byte)
        
        epdconfig.send_command(0x24) # bb b
        for byte in lut.lut_bb:
            epdconfig.send_data(byte)

    def init(self):
        """init()
        epaper hardware initialize
        """
    # 4gray mode init is same as BW mode init
        if (epdconfig.module_init() != 0):
            return -1

        # EPD hardware init start
        epdconfig.reset()

        epdconfig.send_command(0x01) # POWER_SETTING
        epdconfig.send_data(0x03) # VDS_EN, VDG_EN
        epdconfig.send_data(0x00) # VCOM_HV, VGHL_LV[1], VGHL_LV[0]
        epdconfig.send_data(0x2b) # VDH
        epdconfig.send_data(0x2b) # VDL
        epdconfig.send_data(0x09) # VDHR
        
        epdconfig.send_command(0x06) # BOOSTER_SOFT_START
        epdconfig.send_data(0x07)
        epdconfig.send_data(0x07)
        epdconfig.send_data(0x17)
        
        # Power optimization
        epdconfig.send_command(0xF8)
        epdconfig.send_data(0x60)
        epdconfig.send_data(0xA5)
        
        # Power optimization
        epdconfig.send_command(0xF8)
        epdconfig.send_data(0x89)
        epdconfig.send_data(0xA5)
        
        # Power optimization
        epdconfig.send_command(0xF8)
        epdconfig.send_data(0x90)
        epdconfig.send_data(0x00)
        
        # Power optimization
        epdconfig.send_command(0xF8)
        epdconfig.send_data(0x93)
        epdconfig.send_data(0x2A)
        
        # Power optimization
        epdconfig.send_command(0xF8)
        epdconfig.send_data(0xA0)
        epdconfig.send_data(0xA5)
        
        # Power optimization
        epdconfig.send_command(0xF8)
        epdconfig.send_data(0xA1)
        epdconfig.send_data(0x00)
        
        # Power optimization
        epdconfig.send_command(0xF8)
        epdconfig.send_data(0x73)
        epdconfig.send_data(0x41)
        
        epdconfig.send_command(0x16) # PARTIAL_DISPLAY_REFRESH
        epdconfig.send_data(0x00)
        epdconfig.send_command(0x04) # POWER_ON
        epdconfig.wait_idle()
        
        epdconfig.send_command(0x00) # PANEL_SETTING
        epdconfig.send_data(0x3F) # KW-BF   KWR-AF    BWROTP 0f
        
        epdconfig.send_command(0x30) # PLL_CONTROL
        epdconfig.send_data(0x3A) # 3A 100HZ   29 150Hz 39 200HZ    31 171HZ
        
        epdconfig.send_command(0x61) #resolution setting
        epdconfig.send_data (self.width >> 8) 
        epdconfig.send_data (self.width & 0xFF)     	 
        epdconfig.send_data (self.height >> 8) 
        epdconfig.send_data (self.height & 0xFF)
        
        epdconfig.send_command(0x82) # VCM_DC_SETTING_REGISTER
        epdconfig.send_data(0x12)
        
        epdconfig.send_command(0x82) # vcom_DC setting
        epdconfig.send_data (0x12)
        
        epdconfig.send_command(0X50) # VCOM AND DATA INTERVAL SETTING			
        epdconfig.send_data(0x97)
        
        return 0

    def clear(self,gray=0xFF):
        """clear(gray)(gray: int)
        clear screen
        """
        self._set_lut(BW)
        epdconfig.send_command(0x10)
        for i in range(0, int(self.width * self.height / 8)):
            epdconfig.send_data(gray)
        epdconfig.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            epdconfig.send_data(gray)
        epdconfig.send_command(0x12)
        epdconfig.wait_idle()
        width, height = self.last_frame.size
        self.last_frame = Image.new('L', (width, height), gray)

    def sleep(self):
        """sleep()
        e-paper to sleep mode
        """
        epdconfig.send_command(0X50)
        epdconfig.send_data(0xf7)
        epdconfig.send_command(0X02)
        epdconfig.send_command(0X07)
        epdconfig.send_data(0xA5)
        epdconfig.module_exit()

    def _get_frame_buffer(self,img,mode,width,height):
        buf_0 = [0x00] * (width * height // 8)
        buf_1 = [0x00] * (width * height // 8)

        img_gray = img.convert('L')

        if mode in [BW,PARTIAL,FAST]:
            img_gray = _pil1bit(img_gray)
        elif mode == GRAY:
            pass
        else:
            raise ValueError('invalid mode')

        imwidth, imheight = img_gray.size
        pixels = img_gray.load()

        if(imwidth == width and imheight == height):
             for y in range(imheight):
                for x in range(imwidth):
                    buf_0[(x + y * width) // 8] |= ((pixels[x,y]>>7) << (~x % 8))
                    buf_1[(x + y * width) // 8] |= ((0b01 & (pixels[x,y]>>6)) << (~x % 8))
        elif(imwidth == height and imheight == width):
             for y in range(imheight):
                for x in range(imwidth):
                    newy = height - x - 1
                    buf_0[(y + newy * width) // 8] |= ((pixels[x,y]>>7) << (~y % 8))
                    buf_1[(y + newy * width) // 8] |= ((0b01 & (pixels[x,y]>>6)) << (~y % 8))
        else:
            raise ValueError('Image must be same size as input \
                ({0}x{1}).' .format(width, height))
        
        bufs=[buf_0,buf_1]
        return bufs

    def display_frame(self,img,mode=BW):
        """display_frame(img,mode)(img: PIL.Image, mode:int)
        draw frame on e-paper
        """
        buf_0, buf_1 = self._get_frame_buffer(img,mode,self.width,self.height)
        self._set_lut(mode)
        if mode == PARTIAL:
            _, buf_0 = self._get_frame_buffer(self.last_frame,mode,self.width,self.height)
        epdconfig.send_command(0x10)
        for i in range(0, int(self.width * self.height / 8)):
            epdconfig.send_data(buf_0[i])
        epdconfig.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            epdconfig.send_data(buf_1[i])
        epdconfig.send_command(0x12) 
        epdconfig.wait_idle()
        self.last_frame = img.convert('L')

    def _send_partial_area(self,x,y,w,l,reflash=False):
        epdconfig.send_data(x >> 8)
        epdconfig.send_data(x & 0xf8)
        epdconfig.send_data(y >> 8)
        epdconfig.send_data(y & 0xff)
        epdconfig.send_data(w >> 8)
        if reflash:
            epdconfig.send_data(w & 0xff)
        else:
            epdconfig.send_data(w & 0xf8)
        epdconfig.send_data(l >> 8)
        epdconfig.send_data(l & 0xff)

    def partial_display_frame(self,img,x_start,y_start,mode=PARTIAL):
        """partial_display_frame(img,x_start,y_start,mode)(img: PIL.Image, x_start:int, y_start:int, mode:int)
        Partial display frame. Different from the display_frame(), this function will only reflash the screen in a specific area, rather than full screen. The area size will depending on your give image.
        This epaper only can reflash a area size equal 255 x 255.
        """
        logger.debug("Trying partial reflash")
        pic_width, pic_height = img.size

        # I don't know why only 255 x 255 can reflash,so add a limit.
        if pic_width > 0XFF or pic_height > 0xFF :
            raise ValueError("partial reflash area only support 255x255")
        
        tmp_frame = self.last_frame.copy()
        tmp_frame.paste(img,(x_start,y_start,x_start+pic_width,y_start+pic_height))

        # X and W should be the multiple of 8
        if self.last_frame.size == (self.height,self.width):
            y_start = _nearest_integer_of_8(y_start)
            pic_height = _nearest_integer_of_8(pic_height,round_up=True)
            x, y, w, l = y_start, x_start, pic_height, pic_width
        else:
            x_start = _nearest_integer_of_8(x_start)
            pic_width = _nearest_integer_of_8(pic_width,round_up=True)
            x, y, w, l = x_start, y_start, pic_width, pic_height

        if ( (x+w) > (self.width - 1)) or ( (y+l) > (self.height - 1)):
              raise ValueError("reflash area is over the display area.")

        #crop
        oldimg = self.last_frame.crop((x_start,y_start,x_start+pic_width,y_start+pic_height))
        newimg = tmp_frame.crop((x_start,y_start,x_start+pic_width,y_start+pic_height))
 
        buf_0, _ = self._get_frame_buffer(oldimg,mode,pic_width,pic_height)
        _, buf_1 = self._get_frame_buffer(newimg,mode,pic_width,pic_height)

        self._set_lut(mode)

        epdconfig.send_command(0x14) # PARTIAL_DATA_START_TRANSMISSION_1(old data)
        self._send_partial_area(x,y,w,l)
        for i in range(0, w * l // 8):
            epdconfig.send_data(buf_0[i])

        epdconfig.send_command(0x15) # PARTIAL_DATA_START_TRANSMISSION_2(new data)
        self._send_partial_area(x,y,w,l)
        for i in range(0, w * l // 8):
            epdconfig.send_data(buf_1[i])

        epdconfig.send_command(0x16) # PARTIAL_DISPLAY_REFRESH
        self._send_partial_area(x,y,w,l,reflash=True)
        epdconfig.wait_idle()
        self.last_frame = tmp_frame.convert('L')

        




        


