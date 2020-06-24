# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
import board
import adafruit_pcf8591

import adafruit_pcf8591.pcf8591 as PCF
from adafruit_pcf8591.analog_in import AnalogIn

VOLTAGE_LEVEL = 3.3
i2c = board.I2C()
pcf = PCF.PCF8591(i2c)

pcf_in_0 = AnalogIn(pcf, PCF.P0)
while True:
    raw_value = pcf_in_0.value
    scaled_value = (raw_value / 65535) * VOLTAGE_LEVEL

    print("Pin 0: %0.2fV" % (scaled_value))
    print("")
    time.sleep(1)
