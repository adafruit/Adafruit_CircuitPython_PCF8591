# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_pcf8591`
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

# from adafruit_register.i2c_struct import UnaryStruct
# from adafruit_register.i2c_struct_array import StructArray
# from adafruit_register.i2c_bit import RWBit

_PCF8591_DEFAULT_ADDR = const(0x48)  # PCF8591 Default Address
_PCF8591_ENABLE_DAC = const(0x40)  # control bit for having the DAC active


class PCF8591:
    """Driver for the PCF8591 DAC & ADC Combo breakout.
    :param ~busio.I2C i2c_bus: The I2C bus the PCF8591 is connected to.
    :param address: The I2C device address for the sensor. Default is ``0x28``.
    """

    def __init__(self, i2c_bus, address=_PCF8591_DEFAULT_ADDR):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)
        self._dacval = 0
        self._dacenable = False
        self._buffer = bytearray(2)

    def analog_read(self, adcnum):
        """Read an analog value from one of the four ADC inputs

        :param adcnum The single-ended ADC to read from, 0 thru 3
        """
        self._buffer = bytearray(2)
        if self._dacenable:
            self._buffer[0] = _PCF8591_ENABLE_DAC
            self._buffer[1] = self._dacval

        # adcnum cannot be larger than 3
        adcnum = min(adcnum, 3)
        self._buffer[0] |= adcnum & 0x3

        with self.i2c_device as i2c:
            i2c.write_then_readinto(self._buffer, self._buffer)
        return unpack_from(">B", self._buffer[1:])[0]


# /**
#  * Initialises the I2C bus, and finds the PCF8591 on the bus
#  *
#  * @param i2caddr   The I2C address to use for the sensor.
#  * @param  *theWire Optional wire interface, defaults to &Wire
#  * @return True if initialisation was successful, otherwise False.
#  */
# bool Adafruit_PCF8591::begin(uint8_t i2caddr, TwoWire *theWire) :
#   if (self.i2c_device) :
#     delete self.i2c_device; // remove old interface
#   }

#   self.i2c_device = new Adafruit_I2CDevice(i2caddr, theWire);

#   if (!self.i2c_device->begin()) :
#     return false;
#   }

#   return true;
# }


# void Adafruit_PCF8591::enableDAC(bool enable) :# /**
# """ Enables the DAC output or sets it to tri-state / high-Z"""
#  *
#  * @param enable Flag for desired DAC state
#  */
#   self._dacenable = enable;
#   this->analogWrite(_dacval);
# }


# void Adafruit_PCF8591::analogWrite(uint8_t output) :# /**
#  * Writes a uint8_t value to the DAC output
#  *
#  * @param output The value to write: 0 is GND and 255 is VCC
#  */
#   uint8_t self._buffer[2] = :0, 0};
#   if (self._dacenable) :
#     self._buffer[0] = _PCF8591_ENABLE_DAC;
#     self._buffer[1] = output;
#   }
#   _dacval = output;
#   self.i2c_device->write(self._buffer, 2);
# }
