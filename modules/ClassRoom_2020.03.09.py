import spidev
import time
import os
import RPi.GPIO as GPIO

# open SPI bus (SPI needs to be enabled in raspi-config)
spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# set up the pins
led1Pin = 22
led2Pin = 27
led3Pin = 17
# button = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(led1Pin, GPIO.OUT)
GPIO.setup(led2Pin, GPIO.OUT)
GPIO.setup(led3Pin, GPIO.OUT)

# function to read SPI date from MCP3008 chip
# channel must be an integer 0-7
def ReadChannel(channel):
	if channel > 7 or channel < 0:
		return -1
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8)+adc[2]
	return data


thresholdValues = [0,0,0] # parameter to store the trigger levels
hallValues = [0,0,0] #store the Hall effect sensor readings in an array


# before entering the main while loop, measure the hall effect levels and set

for i in range (3):
	#read the hall effect sensor data
	hallValues[i] = ReadChannel(i)
	thresholdValues[i] = int(hallValues[i]*1.05) # 105% to introduce debounce

try:
	while True:
		for i in range (3):
			#read the hall effect sensor data
			hallValues[i] = ReadChannel(i)

			#print out results
			print "Opening", i+1, "Reading =", hallValues[i], "Threshold =", thresholdValues[i]


	# The threshold value is set at 80% below the calibated value.
	# When the sensor detects 90% of the normal value, it will change the led
	# To prevent flicker around the threshold point, add 5% to the threshold
	# when returning the led to the original state. If the value sits between
	# these two values, the led will simply retain its original state

		if hallValues[0]>thresholdValues[0]:
			GPIO.output(led1Pin, GPIO.HIGH)
		elif hallValues[0]<thresholdValues[0]*1.05:
			GPIO.output(led1Pin, GPIO.LOW)
		
		if hallValues[1]>thresholdValues[1]:
			GPIO.output(led2Pin, GPIO.HIGH)
		elif hallValues[1]<thresholdValues[1]*1.05:
			GPIO.output(led2Pin, GPIO.LOW)
			
		if hallValues[2]>thresholdValues[2]:
			GPIO.output(led3Pin, GPIO.HIGH)
		elif hallValues[2]<thresholdValues[2]*1.05:
			GPIO.output(led3Pin, GPIO.LOW)
		time.sleep(0.1) # this delay reduced the CPU utilisation from 100% to approx 50%
except KeyboardInterrupt:
	pass
	
GPIO.cleanup()
print("released GPIO")
time.sleep(2)
