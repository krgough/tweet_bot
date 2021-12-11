#!/bin/env python3
"""
TMP75b - Configure and read temperature from device
"""

import time
import logging
import smbus2


LOGGER = logging.getLogger(__file__)

DEV_BUS = 1
DEV_ADDR = 0x48  # I2C address for TMP75B test board (ADDR = 000)
TEMP_REG = 0x00
CONFIG_REG = 0x01

# Config Reg Bits
ONE_SHOT = 0x80
SHUTDOWN = 0x01

try:
    BUS = smbus2.SMBus(DEV_BUS)
except FileNotFoundError:
    # For testing we just create a fake bus
    BUS = None


def read_config_reg(addr=DEV_ADDR):
    """ Config register is 0x01
        BIT 15 = One Shot.  0=Continuous, 1=One-Shot
        BIT 14 = CR --- Conversion Rate 0h=37Hz (def), 1h=18Hz, 2h=9Hz, 3h=4Hz
        BIT 13 = CR /
        BIT 12 = FQ --- Fault queue to trigger ALERT pin.
        BIT 11 = FQ /   0h=1fault, 1h=2faults, 2h=4fault, 3h=6faults
                        Numer of readings that exceed T_high or T_low before
                        ALERT is set
        BIT 10 = Alert Polarity.  0h = active low, 1h active high
        BIT  9 = Thermostat Mode. 0h=Alert is comparator mode,
                                  1h=Alert is interrupt mode
        BIT  8 = Shutdown.  0h=Continuous coversion, 1h=Shutdown mode
        BIT 7-0 = Reserved (0xFF)

        To use one-shot.
        1) Set shutdown bit to put device in shutdown mode.
        2) To trigger a conversion write '1' to one-shot bit
        3) Serial interface always active so temp register can be read back.

        Since lower bits are reserved we only read the MS bits
    """
    return BUS.read_word_data(addr, CONFIG_REG)


def set_shutdown_mode(addr=DEV_ADDR):
    """ Set the shutdown bit.  Device draw 3uA.  Serial IF still operates.
    """
    cfg = read_config_reg()
    return BUS.write_byte_data(addr, CONFIG_REG, cfg | SHUTDOWN)


def set_one_shot(addr=DEV_ADDR):
    """ Setting one shot starts a single conversion
        Device returns to shutdown after
    """
    cfg = read_config_reg()
    return BUS.write_byte_data(addr, CONFIG_REG, cfg | ONE_SHOT)


def convert_raw_temp_to_float(raw_temp, bits=12):
    """ LSB is temp in degree resolution 1'C
        Represented in 2s complement
        USB upper 4 bits are fractional temp
        USB lower 4 bits are reserved
        1111 xxxx  1 111 1111
          |  |     | |
          |  |     | 0xEF = 127
          |  |     sign i.e. -ve
          |  reserved bits
          Fractional part = 15/16 = 0.9375
          1111xxxx 11111111 = -127.09375
          0000xxxx 00000000 = 0
          1111xxxx 01111111 = -0.0625
          0000xxxx 10000000 = -128
    """
    int_temp = (raw_temp & 0xFF) << 8
    frac_temp = (raw_temp & 0xF000) >> 8
    temp_float = ((int_temp + frac_temp) >> 4)

    # If the number is negative then convert from 2s Complement
    if temp_float & (1 << (bits-1)):
        temp_float = temp_float - (1 << bits)

    temp_float = temp_float / 16

    return temp_float


def read_temperature(addr=DEV_ADDR, one_shot=True):
    """ If one_shot then we need to start a conversion and
        wait for it to compete before reading temperature
    """
    if one_shot:
        set_one_shot()
        # Fastest conversion time is 37Hz ie approx 30ms
        # so we will wait 100ms ro be sure
        time.sleep(0.1)
    raw_temp = BUS.read_word_data(addr, TEMP_REG)
    return convert_raw_temp_to_float(raw_temp)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(levelname)s:%(filename)s:%(asctime)s: %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

    print(f"{read_config_reg():016b}")
    set_shutdown_mode()

    while True:
        print(f"{read_config_reg():016b}")
        print(read_temperature(one_shot=True))
        time.sleep(1)
