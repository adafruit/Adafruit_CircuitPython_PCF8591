# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import board
from adafruit_pcf8591.pcf8591 import PCF8591

VOLTAGE_LEVEL = 3.3
i2c = board.I2C()
pcf = PCF8591(i2c)

channel_a = 0
channel_b = 1

while True:

    read_value = pcf.analog_read(channel_a)
    scaled_value = (read_value / 255) * VOLTAGE_LEVEL

    print("Channel: %d %0.2fV" % (channel_a, scaled_value))
    print("")
    time.sleep(0.1)

    read_value = pcf.analog_read(channel_b)
    scaled_value = (read_value / 255) * VOLTAGE_LEVEL

    print("Channel: %d %0.2fV" % (channel_b, scaled_value))
    print("")
    print("*" * 20)
    time.sleep(1)
