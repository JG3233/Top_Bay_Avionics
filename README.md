# Top_Bay_Avionics
A simple Python Program built to retrieve data from sensors in the top bay of a rocket and save them to a file as well as sending the data to the base station over an RF module. Will additionally activate a servo related to the payload deployment dependant on the data from the sensors.

### Top_Bay.py
>The primary file that will run on boot to get data from the GPS and altimeter and write the to a file based on time and over the RF for real-time data. Programmed for a Raspberry Pi Zero connected via USB OTG.

### Test Files
>Allows easy testing for each individual component in the communication subsytem.

##### Disclaimer
>Written for use in NASA USLI by WURocketry's first ever rocket, Pioneer. Authored by Jacob Gilhaus with many thanks to Adafruit's Circuit Python testing code.
