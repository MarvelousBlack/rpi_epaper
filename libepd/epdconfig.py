"""epdconfig a library to setting edp """
# Copyright (C) 2020 megumifox <i@megumifox.com>
# This file is heavily modified from Waveshare epdconfig.py

# original copyright information below:

# /*****************************************************************************
# * | File        :	  epdconfig.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2019-06-21
# * | Info        :   
# ******************************************************************************
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
import sys
import time

# For RPI 
import spidev
import RPi.GPIO as GPIO

# Pin definition
RST_PIN         = 23
DC_PIN          = 25
CS_PIN          = 8
BUSY_PIN        = 24
SPI_BUS         = 0
SPI_DEVICE      = 0

SPI = spidev.SpiDev()
logger = logging.getLogger('epdconfig')

def digital_write(pin, value):
    GPIO.output(pin, value)

def digital_read(pin):
    return GPIO.input(pin)

def delay_ms(delaytime):
        time.sleep(delaytime / 1000.0)

def spi_writebyte(data):
        SPI.writebytes(data)

def module_init():
    logger.debug("Open and setting SPI")
    SPI.open(SPI_BUS,SPI_DEVICE)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(RST_PIN, GPIO.OUT)
    GPIO.setup(DC_PIN, GPIO.OUT)
    GPIO.setup(CS_PIN, GPIO.OUT)
    GPIO.setup(BUSY_PIN, GPIO.IN)
    SPI.max_speed_hz = 4000000
    SPI.mode = 0b00
    return 0

def module_exit():
      logger.debug("Close SPI")
      SPI.close()

      logger.debug("Close 5V, EDP Module enters 0 power consumption ...")
      GPIO.output(RST_PIN, GPIO.LOW)
      GPIO.output(DC_PIN, GPIO.LOW)

      GPIO.cleanup()

def send_command(command):
    digital_write(DC_PIN, GPIO.LOW)
    digital_write(CS_PIN, GPIO.LOW)
    spi_writebyte([command])
    digital_write(CS_PIN, GPIO.HIGH)

def send_data(data):
    digital_write(DC_PIN, GPIO.HIGH)
    digital_write(CS_PIN, GPIO.LOW)
    spi_writebyte([data])
    digital_write(CS_PIN, GPIO.HIGH)

# Hardware reset
def reset():
    digital_write(RST_PIN, GPIO.HIGH)
    delay_ms(200)
    digital_write(RST_PIN, GPIO.LOW)
    delay_ms(200)
    digital_write(RST_PIN, GPIO.HIGH)
    delay_ms(200)

def wait_idle():
    logger.debug("Waitting e-Paper")
    #send_command(0x71)
    while(digital_read(BUSY_PIN) == GPIO.LOW):      #  LOW: idle, HIGH: busy
        delay_ms(100)
    logger.debug("E-Paper is idele")
