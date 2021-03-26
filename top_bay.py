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

from adafruit_servokit import ServoKit
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
    baudrate = 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1            
)

# Setup servo to release payload
kit = ServoKit(channels=16)
kit.servo[4].set_pulse_width_range(553,2520)

try:
    uartRF.write(str.encode('\nWURocketry\nreal-time data extraction\n\n'))
    f.write('\nWURocketry\nreal-time data extraction\n\n')
    time.sleep(1)
except:
    pass

# set base values for servo usage
ground_alt = -1
fall_count = 0
while ground_alt < 0 or ground_alt > 250:
    try:
        ground_alt = bmp.altitude
    except:
        pass

current_alt = ground_alt

# TEST VALUE
#current_alt = 400
    
base_time = time.monotonic()
last_print = time.monotonic()

while True:
    try:        
        #first check to deploy servo
        prev_alt = current_alt            
        current_alt = bmp.altitude
        
        #TEST VALUE
        #current_alt -= 1

        if current_alt < prev_alt:
            fall_count += 1
        else:
            fall_count = 0

        if fall_count > 10 and current_alt > ground_alt + 50 and current_alt - ground_alt < 200:
            kit.servo[4].angle = 69
        time.sleep(.1) #very brief sleep to spread out alt measurements
    except:
        pass

    try:
        # move on to comm sys tasks
        gps.update()
        # Every second print out current location details if there's a fix.
        current = time.monotonic()
        if current - last_print >= 1.0:
            last_print = current
            f.write("Time: {:8.2f}\n".format(time.monotonic()-base_time))
            uartRF.write(str.encode("Time: {:8.2f}\n".format(time.monotonic()-base_time)))
        
            if not gps.has_fix:
                # Try again if we don't have a fix yet.
                f.write("Waiting for fix...\n")
            else:
                #save data to black box flight_log.txt file and send over RF
                f.write("Latitude: {0:.6f} degrees\n".format(gps.latitude))
                uartRF.write(str.encode("Lat: {0:.3f} deg\n".format(gps.latitude)))
                f.write("Longitude: {0:.6f} degrees\n".format(gps.longitude)) 
                uartRF.write(str.encode("Long: {0:.3f} deg\n".format(gps.longitude)))
                if gps.altitude_m is not None:
                    f.write("Altitude: {} meters\n".format(gps.altitude_m))
                    uartRF.write(str.encode("Alt: {} m\n".format(gps.altitude_m)))
        
            # Always write bmp data
            #uartRF.write(str.encode("Time: {:8.2f}\n".format(time.monotonic()-base_time)))
            f.write("Pressure: {:6.4f}  Temperature: {:5.2f}\n".format(bmp.pressure, bmp.temperature))
            f.write("Altitude: {} meters".format(bmp.altitude))
            f.write("\n========================\n")
        
            # print(".") #heartbeat for testing
            # Also write bmp data over UART to RF
            #uartRF.write(str.encode("Pressure: {:6.4f}  Temp: {:5.2f}\n".format(bmp.pressure, bmp.temperature)))
            uartRF.write(str.encode("BMP Alt: {:6.1f} m\n\n".format(bmp.altitude)))
    except:
        pass

