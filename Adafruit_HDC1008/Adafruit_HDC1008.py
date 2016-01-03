#!/usr/bin/python3

"""
HDC1008 - A Python class for querying a HDC1008
Temperature and Humidity Sensor created by Adafruit #2635 using the
Adafruit_I2C Python library.

The HDC1008 class code was originally created and shared on Stackoverflow
at the following web address

https://stackoverflow.com/questions/32656722/python-can-i-read-two-bytes-in-one-transaction-with-the-smbus-module

It has been reproduced and modified here under the terms of the Creative Commons
Attribution Share Alike licence as explained on Stack Exchange

https://stackexchange.com/legal

Credit goes to the following people for the creation of this class

kfricke (https://github.com/kfricke)
  Work on micropython-hdc1008, which informed initial version of this class
(16-06-2015)

Walter (https://stackoverflow.com/users/5351300/walter)
  Incomplete creation of HDC1008, shared on stackoverflow and, based on work by kfricke
(18-09-2015)

Romke (https://stackoverflow.com/users/5413479/romke)  
  Working version of HDC1008 on stackoverflow, based on work of Walter
(6-10-2015)

Damien Clark - Porting of Romke's version from Stackoverflow to Adafruit's I2C library
(03-01-2016)

It is an initial working implementation that can read temperature and humidity measurements

_TODO_
. Implement fetching of temperature and humidity in single i2c transaction
. Implement precision features for the measurements
. Implement features to control the heater

"""

import time
from Adafruit_I2C import Adafruit_I2C

# ===========================================================================
# HDC1008 Class
# ===========================================================================

class HDC1008:
	
  #Registers
  REG_TEMP =   0
  REG_HUMID =  1
  REG_CONFIG = 2

  #Default Bus
  I2C_BUS = 1

  # Configuration bits for config register
  CFG_RST = 1<<15
  CFG_MODE_SINGLE = 0 << 12
  CFG_MODE_BOTH = 1 << 12

  #Default I2C address for HDC1008
  ADDRESS = 0x40

  # Constructor
  def __init__(self, address=ADDRESS):
     self.i2c = Adafruit_I2C(address)
     self.address = address

  def readTemperature(self):
    # configure the HDC1008 for one reading
    config = 0
    config |= self.CFG_MODE_SINGLE
    self.i2c.write16(self.REG_CONFIG, config)

    # now let's ask for a temperature reading
    self.i2c.writeRaw8(self.REG_TEMP)
    time.sleep(0.015)

    #get the reading back from the thing
    raw = self.i2c.readRaw8()
    raw = (raw<<8) + self.i2c.readRaw8()

    #use TI's formula to turn it into people numbers
    temperature = (raw/65536.0)* 165  - 40


    #convert temp to farenheid
    #temperature = temperature * (9.0/5.0) + 32
    return temperature

  def readHumidity(self):
    # configure the HDC1008 for one reading
    config = 0
    config |= self.CFG_MODE_SINGLE
    self.i2c.write16(self.REG_CONFIG, config)

    # now let's ask for a humidity reading
    self.i2c.writeRaw8(self.REG_HUMID)
    time.sleep(0.015)

    #get the reading back from the thing
    raw = self.i2c.readRaw8()
    raw = (raw<<8) + self.i2c.readRaw8()

    hum=(raw/(2.0**16))*100
    return hum
