#!/bin/env python3

import time
# import smbus2

DEV_BUS = 1
DEV_ADDR = 0x48  # I2C address for TMP75B test board (ADDR = 000)
# bus = smbus2.SMBus(DEV_BUS)

# For testing we just create a fake bus
bus = None


def convert_raw_temp_to_float(raw_temp, bits=12):
    # LSB is temp in degree resolution 1'C
    # Represented in 2s complement
    # USB upper 4 bits are fractional temp
    # USB lower 4 bits are reserved
    # 1111 xxxx  1 111 1111
    #   |  |     | |
    #   |  |     | 0xEF = 127
    #   |  |     sign i.e. -ve
    #   |  reserved bits
    #   Fractional part = 15/16 = 0.9375
    #
    #   1111xxxx 11111111 = -127.09375
    #   0000xxxx 00000000 = 0
    #   1111xxxx 01111111 = -0.0625
    #   0000xxxx 10000000 = -128

    int_temp = (raw_temp & 0xFF) << 8
    frac_temp = (raw_temp & 0xF000) >> 8
    temp_float = ((int_temp + frac_temp) >> 4)

    # If the number is negative then convert from 2s Complement
    if temp_float & (1 << (bits-1)):
        temp_float = temp_float - (1 << bits)

    temp_float = temp_float / 16

    return temp_float


def read_temperature(dev_addresss=DEV_ADDR):
    raw_temp = bus.read_word_data(DEV_ADDR, 0x00)
    return convert_raw_temp_to_float(raw_temp)


if __name__ == "__main__":
    while True:
        print(read_temperature(DEV_ADDR))
        time.sleep(1)
