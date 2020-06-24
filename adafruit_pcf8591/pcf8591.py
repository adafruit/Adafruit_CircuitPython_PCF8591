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
P0 = 0
P1 = 1
P2 = 2
P3 = 3

DAC_OUT = 0

class PCF8591:
    """Driver for the PCF8591 DAC & ADC Combo breakout.

    :param ~busio.I2C i2c_bus: The I2C bus the PCF8591 is connected to.
    :param address: The I2C device address for the sensor. Default is ``0x28``.

    """

    def __init__(self, i2c_bus, address=_PCF8591_DEFAULT_ADDR):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)
        self._dacval = 0
        self._dac_enabled = False
        self._buffer = bytearray(2)

    def analog_read(self, channel):
        """Read an analog value from one of the four ADC inputs

          param: :adcnum The single-ended ADC to read from, 0 thru 3
        """
        print("passed in channel", channel)
        self._buffer = bytearray(2)
        if self._dac_enabled:
            self._buffer[0] = _PCF8591_ENABLE_DAC
            self._buffer[1] = self._dacval

        # adc_channel cannot be larger than 3
        channel = min(channel, 3)
        print("using channel", channel)
        self._buffer[0] |= channel & 0x3
        # TODO: Add an Argument error raise here

        with self.i2c_device as i2c:
            i2c.write_then_readinto(self._buffer, self._buffer)
        return unpack_from(">B", self._buffer[1:])[0]

    @property
    def dac_enabled(self):
        """ Enables the DAC when True, or sets it to tri-state / high-Z when False
        """
        return self._dac_enabled

    @dac_enabled.setter
    def dac_enabled(self, enable_dac):

        self._dac_enabled = enable_dac
        self.analog_write(self._dacval)

    def analog_write(self, value):
        """Writes a uint8_t value to the DAC output

      param: :output The value to write: 0 is GND and 255 is VCC

      """

        self._buffer = bytearray(2)
        if self._dac_enabled:
            self._buffer[0] = _PCF8591_ENABLE_DAC
            self._buffer[1] = value
        self._dacval = value
        with self.i2c_device as i2c:
            i2c.write_then_readinto(self._buffer, self._buffer)


class Channel:
    """An instance of a single channel for a multi-channel DAC.

    **All available channels are created automatically and should not be created by the user**"""

    def __init__(self, dac_instance, cache_page, index):
        self._vref = cache_page["vref"]
        self._gain = cache_page["gain"]
        self._raw_value = cache_page["value"]
        self._dac = dac_instance
        self.channel_index = index

    @property
    def normalized_value(self):
        """The DAC value as a floating point number in the range 0.0 to 1.0."""
        return self.raw_value / (2 ** 12 - 1)

    @normalized_value.setter
    def normalized_value(self, value):
        if value < 0.0 or value > 1.0:
            raise AttributeError("`normalized_value` must be between 0.0 and 1.0")

        self.raw_value = int(value * 4095.0)

    @property
    def value(self):
        """The 16-bit scaled current value for the channel. Note that the MCP4728 is a 12-bit piece
        so quantization errors will occour"""
        return self.normalized_value * (2 ** 16 - 1)

    @value.setter
    def value(self, value):
        if value < 0 or value > (2 ** 16 - 1):
            raise AttributeError(
                "`value` must be a 16-bit integer between 0 and %s" % (2 ** 16 - 1)
            )

        # Scale from 16-bit to 12-bit value (quantization errors will occur!).
        self.raw_value = value >> 4

    @property
    def raw_value(self):
        """The native 12-bit value used by the DAC"""
        return self._raw_value

    @raw_value.setter
    def raw_value(self, value):
        if value < 0 or value > (2 ** 12 - 1):
            raise AttributeError(
                "`raw_value` must be a 12-bit integer between 0 and %s" % (2 ** 12 - 1)
            )
        self._raw_value = value
        # disabling the protected access warning here because making it public would be
        # more confusing
        self._dac._set_value(self)  # pylint:disable=protected-access

    @property
    def gain(self):
        """Sets the gain of the channel if the Vref for the channel is ``Vref.INTERNAL``.
        **The gain setting has no effect if the Vref for the channel is `Vref.VDD`**.

        With gain set to 1, the output voltage goes from 0v to 2.048V. If a channe's gain is set
        to 2, the voltage goes from 0v to 4.096V. `gain` Must be 1 or 2"""
        return self._gain

    @gain.setter
    def gain(self, value):
        if not value in (1, 2):
            raise AttributeError("`gain` must be 1 or 2")
        self._gain = value - 1
        self._dac.sync_gains()

    @property
    def vref(self):
        """Sets the DAC's voltage reference source. Must be a ``VREF``"""
        return self._vref

    @vref.setter
    def vref(self, value):
        if not Vref.is_valid(value):
            raise AttributeError("range must be a `Vref`")
        self._vref = value
        self._dac.sync_vrefs()
