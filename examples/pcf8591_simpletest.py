# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
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
    for channel_number in range(4):
        read_value = pcf.analog_read(channel_number)
        scaled_value = (read_value / 255) * VOLTAGE_LEVEL

        print("Channel: %d %0.2fV" % (channel_number, scaled_value))
    print("")
    time.sleep(1)
