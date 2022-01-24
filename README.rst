Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-pcf8591/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/pcf8591/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_PCF8591/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_PCF8591/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

ADC+DAC Combo


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================


On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-pcf8591/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-pcf8591

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-pcf8591

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-pcf8591

Usage Example
=============

.. code-block:: python3

    import time
    import board

    import adafruit_pcf8591.pcf8591 as PCF
    from adafruit_pcf8591.analog_in import AnalogIn
    from adafruit_pcf8591.analog_out import AnalogOut

    ############# AnalogOut & AnalogIn Example ##########################
    #
    # This example shows how to use the included AnalogIn and AnalogOut
    # classes to set the internal DAC to output a voltage and then measure
    # it with the first ADC channel.
    #
    # Wiring:
    # Connect the DAC output to the first ADC channel, in addition to the
    # normal power and I2C connections
    #
    #####################################################################
    i2c = board.I2C()
    pcf = PCF.PCF8591(i2c)

    pcf_in_0 = AnalogIn(pcf, PCF.A0)
    pcf_out = AnalogOut(pcf, PCF.OUT)

    while True:

        print("Setting out to ", 65535)
        pcf_out.value = 65535
        raw_value = pcf_in_0.value
        scaled_value = (raw_value / 65535) * pcf_in_0.reference_voltage

        print("Pin 0: %0.2fV" % (scaled_value))
        print("")
        time.sleep(1)



Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/pcf8591/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_PCF8591/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
