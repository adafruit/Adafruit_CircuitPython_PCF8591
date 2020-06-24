# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import board
from adafruit_pcf8591.pcf8591 import PCF8591

VOLTAGE_LEVEL = 3.3
DAC_VALUE = 255
i2c = board.I2C()

pcf = PCF8591(i2c)
print("enabling DAC")
pcf.dac_enabled = True
while True:
    print("Setting DAC to", 255)
    pcf.analog_write(255)
    print("Reading channel 3")
    read_value = pcf.analog_read(3)
    scaled_value = (read_value / 255) * VOLTAGE_LEVEL

    print("Channel 3: %0.2fV" % (scaled_value))
    print("")
    time.sleep(0.5)
    print("Setting DAC to", 0)
    pcf.analog_write(0)

    print("Reading channel 3")
    read_value = pcf.analog_read(3)
    scaled_value = (read_value / 255) * VOLTAGE_LEVEL

    print("Channel 3: %0.2fV" % (scaled_value))
    print("")

    time.sleep(1.0)
