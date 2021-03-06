#!/usr/bin/python3

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Modified GPS module demonstration for 2021 NSLI 
# Authored by Jacob Gilhaus of WURocketry
# Washington University in St. Louis

import datetime
import time
import board
import busio

import adafruit_gps
import adafruit_bmp3xx
import serial

#altimeter connected to pi over i2c
i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c, 118)

bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

#gps also connected to pi via i2c
i2c = board.I2C()
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")

base_time = time.monotonic()
last_print = time.monotonic()

falling = False
fall_count = 0
ground_alt = bmp.altitude
#current_alt = ground_alt

#testing value
current_alt = 1000

while True:
    #try:
    prev_alt = current_alt
    #current_alt = bmp.altitude
    
    # Testing Value
    current_alt -= 1
    #print(current_alt)

    if current_alt < prev_alt:
        fall_count += 1
        print(fall_count)
    else:
        fall_count = 0

    if fall_count > 10 and current_alt > ground_alt + 200:
        # turn servo
        print('deploying payload')

    #except:
     #   exit
      #  pass

