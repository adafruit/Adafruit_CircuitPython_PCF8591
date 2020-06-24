# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import board
from adafruit_pcf8591.pcf8591 import PCF8591

################ read/DAC Example #####################
#
# This example shows how to use a PCF8591 instance to set the voltage output by the included DAC.
#
# Wiring:
# Connect the DAC output to the first ADC channel, in addition to the
# normal power and I2C connections
#
########################################
i2c = board.I2C()

pcf = PCF8591(i2c)
print("enabling DAC")
pcf.dac_enabled = True
while True:
    print("Setting DAC to", 255)
    pcf.write(255)
    print("Reading channel 0")
    read_value = pcf.read(0)
    scaled_value = (read_value / 255) * pcf.reference_voltage

    print("Channel 0: %0.2fV" % (scaled_value))
    print("")
    time.sleep(0.5)
    print("Setting DAC to", 0)
    pcf.write(0)

    print("Reading channel 0")
    read_value = pcf.read(0)
    scaled_value = (read_value / 255) * pcf.reference_voltage

    print("Channel 3: %0.2fV" % (scaled_value))
    print("")

    time.sleep(1.0)
