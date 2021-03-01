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

# get current time for filename
now = datetime.datetime.now()

# Open log file to write flight data
f = open('flight_log_' + now.strftime("%m-%d-%y_%H:%M:%S") + '.txt', 'w')

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

#setup for RF over UART
uartRF = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1            
 )


base_time = time.monotonic()
last_print = time.monotonic()

while True:
    #write data over RF
    #uartRF.write(str.encode("Time: {:8.2f}\n".format(time.monotonic()-base_time)))
    #uartRF.write(str.encode("Pressure: {:6.4f}  Temperature: {:5.2f}\n".format(bmp.pressure, bmp.temperature)))
    #uartRF.write(str.encode("Altitude: {} meters".format(bmp.altitude)))
    #uartRF.write(str.encode("\n========================================\n"))

    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        f.write("Time: {:8.2f}\n".format(time.monotonic()-base_time))
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            f.write("Waiting for fix...\n")
        else:
        #save data to black box flight_log.txt file
            f.write("Latitude: {0:.6f} degrees\n".format(gps.latitude))
            f.write("Longitude: {0:.6f} degrees\n".format(gps.longitude)) 
            if gps.altitude_m is not None:
                f.write("Altitude: {} meters\n".format(gps.altitude_m))
        f.write("Pressure: {:6.4f}  Temperature: {:5.2f}\n".format(bmp.pressure, bmp.temperature))
        f.write("Altitude: {} meters".format(bmp.altitude))
        f.write("\n========================================\n")
        # print(".") #heartbeat for testing


