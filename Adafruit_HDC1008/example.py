#!/usr/bin/python3

from Adafruit_HDC1008 import HDC1008

# ===========================================================================
# Example Code
# ===========================================================================

#Get sensor object at it's default i2c address
Sensor=HDC1008()

# Print the temperature
print(Sensor.readTemperature())

# Print the humidity
print(Sensor.readHumidity())
