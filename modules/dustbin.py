import spidev
import time
import os
import RPi.GPIO as GPIO

# open SPI bus (SPI needs to be enabled in raspi-config)
spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# set up the pins
greenLed = 13
redLed = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(greenLed, GPIO.OUT)
GPIO.setup(redLed, GPIO.OUT)

# function to read SPI date from MCP3008 chip
# channel must be an integer 0-7
def ReadChannel(channel):
    if channel > 7 or channel < 0:
        return -1
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8)+adc[2]
    return data


lidSensor = 0
fullSensor = 0
lidTrigger = 0
fullTrigger = 0

# before entering the main while loop, measure the light levels and set
# this as 'normal'. In the while loop, the button can be pressed to recalibrate

lidSensor = ReadChannel(0)
fullSensor = ReadChannel(1)

lidTrigger = lidSensor * 0.97
fullTrigger = fullSensor * 0.8

lidOpen = False
binFull = False

try:
    while True:
        
        lidSensor = ReadChannel(0)
        fullSensor = ReadChannel(1)
        
        print "Lid Reading =", lidSensor, "     lid Open?", lidOpen, "    Full Reading =", fullSensor, "   Bin Full?", binFull
    # The threshold value is set at 80% below the calibated value.
    # When the LDR detects 90% of the normal value, it will change the led
    # To prevent flicker around the threshold point, add 5% to the threshold
    # when returning the led to the original state. If the value sits between
    # these two values, the led will simply retain its original state

        if lidSensor<lidTrigger and lidOpen == False:
            GPIO.output(greenLed, GPIO.HIGH)
            lidOpen = True
        elif lidSensor>lidTrigger*1.02:
            GPIO.output(greenLed, GPIO.LOW)
            lidOpen = False
        if fullSensor<fullTrigger and binFull == False:
            GPIO.output(redLed, GPIO.HIGH)
            binFull = True
        elif fullSensor>fullTrigger*1.05:
            GPIO.output(redLed, GPIO.LOW)
            binFull = False
        
        time.sleep(0.1) # this delay reduced the CPU utilisation from 100% to approx 50%
except KeyboardInterrupt:
    pass
    
GPIO.cleanup()
print("released GPIO")
time.sleep(2)
