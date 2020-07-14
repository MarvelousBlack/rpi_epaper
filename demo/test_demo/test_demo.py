#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Copyright (C) 2020 megumifox <i@megumifox.com>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from pathlib import Path
import logging
import time
import datetime
from PIL import Image,ImageDraw,ImageFont
import traceback
#Change epd4in2 to you want
from libepd import epd4in2

epd = epd4in2.EPD()

logging.basicConfig(level=logging.DEBUG)

BW = 0x00
GRAY = 0x01
PARTIAL = 0x02
FAST = 0x03

TIMEFORMAT = '%H:%M'
DATEFORMAT = '%m/%d/%Y'
DAYFORMAT = '%A'
font = ImageFont.truetype('NotoSans-Medium.ttf', size=75)
font2 = ImageFont.truetype('NotoSans-Medium.ttf', size=35)
font3 = ImageFont.truetype('NotoSansCJK-Medium.ttc', size=25)

ntime = datetime.datetime.now().strftime(TIMEFORMAT)
ndate = datetime.datetime.now().strftime(DATEFORMAT)
nday = datetime.datetime.now().strftime(DAYFORMAT)

try:
    epd.init()
    epd.clear(0xFF)
    time.sleep(2)

    epd.clear(0x00)
    time.sleep(2)
    
    image_0 = Image.new('L', (epd.width,epd.height), 0xFF)
    draw = ImageDraw.Draw(image_0)
    draw.text((30,0), str(ntime), font = font, fill = 0x80)
    draw.text((2,100), str(ndate), font = font2, fill = 0x40)
    draw.text((55,140), str(nday), font = font3, fill = 0x00)
    epd.display_frame(image_0,BW)
    time.sleep(1)
    
    epd.clear(0xFF)
    time.sleep(1)
    
    epd.display_frame(image_0,GRAY)
    time.sleep(2)
    
    epd.clear()
    image_1 = Image.new('L', (60,60), 0)
    epd.partial_display_frame(image_1,60,60,PARTIAL)
    image_2 = Image.new('L', (30,30), 0)
    epd.partial_display_frame(image_2,00,00,FAST)

finally:
    epd.sleep()
