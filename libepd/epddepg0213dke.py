"""epddepg0213dke - e-paper display library for the depg0213dke 2.3inch e-Paper """
# Copyright (C) 2021 megumifox <i@megumifox.com>


import logging
from . import epdconfig
from .lut_depg0213_dke import Full_LUT


logger = logging.getLogger('epd')

# Display resolution
EPD_WIDTH       = 212
EPD_HEIGHT      = 104

class EPD:
    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT


    def _set_lut(self):
        #epdconfig.send_command(0x32) 
        #for byte in Full_LUT.lut:
        #    epdconfig.send_data(byte)

        # Load otp lut
        epdconfig.send_command(0x18)
        epdconfig.send_data(0x80)
        epdconfig.send_command(0x22)
        epdconfig.send_data(0xB1)
        epdconfig.send_command(0x20)

        epdconfig.wait_idle()
        return 0

    def software_reset(self):
        epdconfig.send_command(0x12)
        epdconfig.wait_idle()
        return 0

    def init(self):
        """init()
        epaper hardware initialize
        """
        if (epdconfig.module_init() != 0):
            return -1
        epdconfig.reset()
        epdconfig.wait_idle()
        self.software_reset()
        # Set Analog Block Control
        epdconfig.send_command(0x74)
        epdconfig.send_data(0x54)
        # Set Digital Block Control
        epdconfig.send_command(0x7E)
        epdconfig.send_data(0x3B)
        # Set display size and driver output 
        epdconfig.send_command(0x01)
        epdconfig.send_data(0xF9)
        epdconfig.send_data(0x00)
        epdconfig.send_data(0x00)
        # Ram data entry mode
        epdconfig.send_command(0x11)
        epdconfig.send_data(0x01)
        # Set Ram X address
        epdconfig.send_command(0x44)
        epdconfig.send_data(0x00)
        epdconfig.send_data(0x0C)
        # Set Ram Y address
        epdconfig.send_command(0x45)
        epdconfig.send_data(0xD3)
        epdconfig.send_data(0x00)
        epdconfig.send_data(0x00)
        epdconfig.send_data(0x00)
        # Set border
        epdconfig.send_command(0x3C)
        epdconfig.send_data(0x01)
        # Set VCOM value
        epdconfig.send_command(0x2C)
        epdconfig.send_data(0x5A)
        # Gate voltage setting
        epdconfig.send_command(0x03)
        epdconfig.send_data(0x17)
        # Source voltage setting
        epdconfig.send_command(0x04)
        epdconfig.send_data(0x41)
        epdconfig.send_data(0xAC)
        epdconfig.send_data(0x32)
        # Frame setting 50hz
        epdconfig.send_command(0x3A)
        epdconfig.send_data(0x02)
        epdconfig.send_command(0x3B)
        epdconfig.send_data(0x0D)
        # Load LUT
        self._set_lut()
        return 0

    def _send_frame(self,buf):
        # Set Ram X address counter
        epdconfig.send_command(0x4E)
        epdconfig.send_data(0x00)
        # Set Ram Y address counter
        epdconfig.send_command(0x4F)
        epdconfig.send_data(0xD3)
        epdconfig.send_data(0x00)
        # Send BW image (104/8*212)
        epdconfig.send_command(0x24)
        for i in buf[0]:
            epdconfig.send_data(i)
        
        # Set Ram X address counter
        epdconfig.send_command(0x4E)
        epdconfig.send_data(0x00)
        # Set Ram Y address counter
        epdconfig.send_command(0x4F)
        epdconfig.send_data(0xD3)
        epdconfig.send_data(0x00)
        # Send RED image (104/8*212)
        epdconfig.send_command(0x26)
        for i in buf[1]:
            epdconfig.send_data(i)
        return 0

    def image_update(self):
        epdconfig.send_command(0x22)
        epdconfig.send_data(0xC7)
        epdconfig.send_command(0x20)
        epdconfig.wait_idle()
        return 0
        
    def clear(self):
        buf_0 = [0xFF] * (self.width * self.height // 8)
        buf_1 = [0x00] * (self.width * self.height // 8)
        buf =[buf_0,buf_1]
        self._send_frame(buf)
        self.image_update()
        return 0

    def sleep(self):
        """sleep()
        e-paper to sleep mode
        """
        epdconfig.send_command(0X10)
        epdconfig.send_data(0x01)
        epdconfig.module_exit()
        return 0
