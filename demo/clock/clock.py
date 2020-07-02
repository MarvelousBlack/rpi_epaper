#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
from pathlib import Path
import logging
import time
import datetime
from PIL import Image,ImageDraw,ImageFont
import traceback
#import locale
sys.path.append(str(Path.cwd().parents[1]))
from libepd import epd2in7

logging.basicConfig(level=logging.INFO)

epd = epd2in7.EPD()
TIMEFORMAT = '%H:%M'
DATEFORMAT = '%m/%d/%Y'
DAYFORMAT = '%A'
font = ImageFont.truetype('NotoSans-Medium.ttf', size=75)
font2 = ImageFont.truetype('NotoSans-Medium.ttf', size=35)
font3 = ImageFont.truetype('NotoSansCJK-Medium.ttc', size=25)
#locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
try:
    epd.init()
    epd.clear(0xFF)
    ntime = datetime.datetime.now().strftime(TIMEFORMAT)
    ndate = datetime.datetime.now().strftime(DATEFORMAT)
    nday = datetime.datetime.now().strftime(DAYFORMAT)
    #Himage= Image.open("background.png")
    Himage = Image.new('L', (epd.height, epd.width), 255) 
    draw = ImageDraw.Draw(Himage)
    draw.text((30,0), str(ntime), font = font, fill = 0)
    draw.text((2,100), str(ndate), font = font2, fill = 0)
    draw.text((55,140), str(nday), font = font3, fill = 0)
    epd.display_frame(Himage)
finally:
    epd.sleep()
