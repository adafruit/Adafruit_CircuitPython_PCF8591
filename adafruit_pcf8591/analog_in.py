# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`analog_in`
==============================
AnalogIn for ADC readings.

* Author(s): Bryan Siepert, adpted from ADS1x15 by Carter Nelson
"""


class AnalogIn:
    """AnalogIn Mock Implementation for ADC Reads."""

    def __init__(self, ads, pin):
        """AnalogIn

        :param ads: The PCF8591 object.
        :param ~digitalio.DigitalInOut pin: Required pin for single-ended.

        """
        self._ads = ads
        self._channel_number = pin

    @property
    def value(self):
        """Returns the value of an ADC pin scaled to a 16-bit integer from the native value."""
        return self._ads.analog_read(self._channel_number) << 8

    # @property
    # def voltage(self):
    #     """Returns the voltage from the ADC pin as a floating point value."""
    #     volts = self.value * _ADS1X15_PGA_RANGE[self._ads.gain] / 32767
    #     return volts
