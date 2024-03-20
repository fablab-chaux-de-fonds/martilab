# https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/data-logger
# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
boot.py file for Pico data logging example. If pin GP0 is connected to GND when
the pico starts up, make the filesystem writeable by CircuitPython.
"""
import board
import digitalio
import storage

write_pin = digitalio.DigitalInOut(board.GP14) # initial to GP0
write_pin.direction = digitalio.Direction.INPUT
write_pin.pull = digitalio.Pull.UP

# If write pin is not connected to ground on start-up, CircuitPython can write to CIRCUITPY filesystem.
if write_pin.value:
    storage.remount("/", readonly=False)
