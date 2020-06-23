# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import board
import adafruit_pcf8591

VOLTAGE_LEVEL = 3.3
i2c = board.I2C()
pcf = adafruit_pcf8591.PCF8591(i2c)

while True:
    read_value = pcf.analog_read(0)
    scaled_value = (read_value / 255) * VOLTAGE_LEVEL
    print("Read value:", read_value, "Scaled measurement: %0.2f V" % scaled_value)
    time.sleep(0.2)
