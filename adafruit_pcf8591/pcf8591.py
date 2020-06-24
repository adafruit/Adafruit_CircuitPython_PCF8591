# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`pcf8591`
================================================================================

ADC+DAC Combo

* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

* `Adafruit PCF8591 Breakout <https://www.adafruit.com/products/45XX>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

 * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
 * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_PCF8591.git"
# from time import sleep
from struct import unpack_from
from micropython import const
import adafruit_bus_device.i2c_device as i2c_device

_PCF8591_DEFAULT_ADDR = const(0x48)  # PCF8591 Default Address
_PCF8591_ENABLE_DAC = const(0x40)  # control bit for having the DAC active

# Pin constants
A0 = 0
A1 = 1
A2 = 2
A3 = 3

OUT = 0


class PCF8591:
    """Driver for the PCF8591 DAC & ADC Combo breakout.

    :param ~busio.I2C i2c_bus: The I2C bus the PCF8591 is connected to.
    :param address: The I2C device address for the sensor. Default is ``0x28``.

    """

    def __init__(self, i2c_bus, address=_PCF8591_DEFAULT_ADDR, reference_voltage=3.3):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)
        self._dacval = 0
        self._dac_enabled = False
        # this is the range supported by the PCF8591
        if 2.5 <= reference_voltage <= 6.0:
            self._reference_voltage = reference_voltage
        else:
            raise ValueError("reference_voltage must be from 2.5 - 6.0")
        self._buffer = bytearray(2)
        print("self.reference_voltage = ", self.reference_voltage)

    @property
    def reference_voltage(self):
        """The voltage level that ADC signals are compared to.
        An ADC value of 65535 will equal `reference_voltage`"""
        return self._reference_voltage

    def read(self, channel):
        """Read an analog value from one of the four ADC inputs

          param: :adcnum The single-ended ADC to read from, 0 thru 3
        """
        self._buffer = bytearray(2)
        if self._dac_enabled:
            self._buffer[0] = _PCF8591_ENABLE_DAC
            self._buffer[1] = self._dacval

        if channel < 0 or channel > 3:
            raise ValueError("channel must be from 0-3")
        # adc_channel cannot be larger than 3
        channel = min(channel, 3)
        self._buffer[0] |= channel & 0x3
        # TODO: Add an Argument error raise here

        with self.i2c_device as i2c:
            i2c.write_then_readinto(self._buffer, self._buffer)
        return unpack_from(">B", self._buffer[1:])[0]

    @property
    def dac_enabled(self):
        """ Enables the DAC when True, or sets it to tri-state / high-Z when False"""
        return self._dac_enabled

    @dac_enabled.setter
    def dac_enabled(self, enable_dac):

        self._dac_enabled = enable_dac
        self.write(self._dacval)

    def write(self, value):
        """Writes a uint8_t value to the DAC output

      param: :output The value to write: 0 is GND and 65535 is VCC

      """

        self._buffer = bytearray(2)
        if self._dac_enabled:
            self._buffer[0] = _PCF8591_ENABLE_DAC
            self._buffer[1] = value
        self._dacval = value
        with self.i2c_device as i2c:
            i2c.write_then_readinto(self._buffer, self._buffer)
