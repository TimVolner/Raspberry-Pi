# Created 6/8/2019 - 11:11 AM
# Last Updated 6/8/2019 - 11:11 AM

# This program currently turns on/off 1 relay, but with slight modification this program can control multiple relays
# This has not been tested on a Ras Pi yet

import os
import glob
import time
import RPi.GPIO as GPIO

# set pin number for relay 1
relay1_pin=11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay_pin,GPIO.OUT)
GPIO.output(relay_pin, GPIO.HIGH)

def read_file_temp():
    
    # locate the file containing temp probe reading
    directory = "/sys/bus/w1/devices/"
    device_fold = glob.glob(directory + "28*")[0]
    device_file = device_fold + "/w1_slave"    
    
    # read the file containing temp probe reading
    with open(device_file, "r") as f:
        data = f.readlines()
    
    return(data)

def read_temp():
    
    # read the file which contains the data necessary to proceed with operation
    data = read_file_temp()
    
    # Wait until temp probe is ready and recording data
    while data[0].strip()[-3:] != "YES":
        time.sleep(0.5)
        data = read_file_temp()
    
    # point the program to a specific position in the file    
    file_position = data[1].find("t=")
    
    # if position in the file will not be out of range, read the temp in Celsius
    if file_position != -1:
        temp = float(data[1][file_position+2:])
        temp = temp / 1000.0
        return(temp)

def main(relay1):
    
    # Get Temperature Probe value
    temp = read_temp()
    
    # if temp is greater than x, turn relay on
    # if temp is less or equal to x, turn relay off
    
    if temp > 24: # change value here to desired temperature setting
        
        # GPIO.LOW and GPIO.HIGH may need to be changed depending on relays used
        GPIO.output(relay1, GPIO.LOW)
        print("Relay on")        
        
    else:
        
        # GPIO.LOW and GPIO.HIGH may need to be changed depending on relays used
        GPIO.output(relay1, GPIO.HIGH)
        print("Relay off")   
        
    # Wait for 5 seconds then run script again
    # This can be removed and program will run non-stop
    # Time can also be changed to any desired value
    # Time is in seconds
    time.sleep(5)    


# Run the program continuously
while True:
    main(relay1_pin)

