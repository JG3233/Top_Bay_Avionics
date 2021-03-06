#!/usr/bin/python3

import serial
import time

print('hello, testing rf file')
counter = 0

uart =  serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1            
 )

while True:
    try:
        uart.write(str.encode("Counting... \n"))
    except IOError as e:
        print('exception', e)
    time.sleep(1)
    counter += 1
    print('.')
    #msg = uart.readline().strip()
    #print(msg)

#device=XBeeDevice("/dev/ttyAMA0", 9600)
#device.open()
# Configure the DIO1_AD1 line of the local device to be Digital output (set high by default).
#device.set_io_configuration(IOLine.DIO1_AD1, IOMode.DIGITAL_OUT_HIGH)

# Configure the DIO2_AD2 line of the local device to be Digital input.
#device.set_io_configuration(IOLine.DIO2_AD2, IOMode.DIGITAL_IN)

#device.send_data_broadcast("Hello XBee world")
#device.close()

print('success')

