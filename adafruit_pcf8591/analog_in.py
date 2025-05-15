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

try:
    import typing

    from typing_extensions import Literal

    from adafruit_pcf8591.pcf8591 import PCF8591
except ImportError:
    pass


class AnalogIn:
    """AnalogIn Mock Implementation for ADC Reads."""

    def __init__(self, pcf: PCF8591, pin: Literal[0, 1, 2, 3]) -> None:
        """AnalogIn

        :param pcf: The PCF8591 object.
        :param int pin: Required ADC channel pin; must be 0-3 inclusive

        """
        self._pcf = pcf
        self._channel_number = pin

    @property
    def voltage(self) -> float:
        """Returns the value of an ADC channel in volts as compared to the reference voltage."""

        if not self._pcf:
            raise RuntimeError("Underlying ADC does not exist, likely due to calling `deinit`")
        raw_reading = self._pcf.read(self._channel_number)
        return ((raw_reading << 8) / 65535) * self._pcf.reference_voltage

    @property
    def value(self) -> int:
        """Returns the value of an ADC channel.
        The value is scaled to a 16-bit integer from the native 8-bit value."""

        if not self._pcf:
            raise RuntimeError("Underlying ADC does not exist, likely due to calling `deinit`")

        return self._pcf.read(self._channel_number) << 8

    @property
    def reference_voltage(self) -> float:
        """The maximum voltage measurable (also known as the reference voltage) as a float in
        Volts. Assumed to be 3.3V but can be overridden using the `PCF8591` constructor
        """
        if not self._pcf:
            raise RuntimeError("Underlying ADC does not exist, likely due to calling `deinit`")
        return self._pcf.reference_voltage

    def deinit(self) -> None:
        """Release the reference to the PCF8591. Create a new AnalogIn to use it again."""
        self._pcf = None
