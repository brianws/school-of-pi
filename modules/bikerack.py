# updated 2020.03.11.22:43
import spidev
import time
import os
import RPi.GPIO as GPIO
import mysql.connector
from datetime import date, datetime, timedelta

# open SPI bus (SPI needs to be enabled in raspi-config)
spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# set up the pins
led1Pin = 16
led2Pin = 20
led3Pin = 12
button = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(led1Pin, GPIO.OUT)
GPIO.setup(led2Pin, GPIO.OUT)
GPIO.setup(led3Pin, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

bike1Docked = False
bike2Docked = False
bike3Docked = False

# function to read SPI date from MCP3008 chip
# channel must be an integer 0-7
def ReadChannel(channel):
	if channel > 7 or channel < 0:
		return -1
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8)+adc[2]
	return data

def SaveToCloud():
	# save value to cloud
	connection = mysql.connector.connect(host='susschool1.csocp6rlrcp1.eu-west-2.rds.amazonaws.com', user='admin', database='susschool', password='h7e48wt^78wE377bhh5*' )
	cursor = connection.cursor()
	now = datetime.now().date()
	year_4_st_marys = 5
	sql = "INSERT INTO susschool_reading(type, amount, area_id, created_date) VALUES(%s, %s, %s, %s)"
	data = ('bike', 1, year_4_st_marys, now)
	result = cursor.execute(sql, data)
	connection.commit()
	cursor.close()
	connection.close()

thresholdValues = [0,0,0] # parameter to store the trigger light level
lightValues = [0,0,0] #store the LDR readings in an array

# before entering the main while loop, measure the light levels and set
# this as 'normal'. In the while loop, the button can be pressed to recalibrate

for i in range (3):
	#read the light sensor data
	lightValues[i] = ReadChannel(i)
	thresholdValues[i] = int(lightValues[i]*0.80) # 80% to introduce debounce

try:
	while True:
		for i in range (3):
			#read the light sensor data
			lightValues[i] = ReadChannel(i)

			#print out results
			print "Bike", i+1, "Reading =", lightValues[i], "Threshold =", thresholdValues[i]

		# if the reset button is pressed, store the new light settings
		if not GPIO.input(button): #if the button is pressed
			for i in range(3):
				thresholdValues[i] = int(lightValues[i]*0.80) # 80% to introduce debounce

	# The threshold value is set at 80% below the calibated value.
	# When the LDR detects 90% of the normal value, it will change the led
	# To prevent flicker around the threshold point, add 5% to the threshold
	# when returning the led to the original state. If the value sits between
	# these two values, the led will simply retain its original state

		if lightValues[0]<thresholdValues[0] and bike1Docked == False:
			GPIO.output(led1Pin, GPIO.HIGH)
			SaveToCloud()
                        bike1Docked = True
		elif lightValues[0]>thresholdValues[0]*1.05:
			GPIO.output(led1Pin, GPIO.LOW)
                        bike1Docked = False

		if lightValues[1]<thresholdValues[1] and bike2Docked == False:
			GPIO.output(led2Pin, GPIO.HIGH)
                        SaveToCloud()
                        bike2Docked = True
		elif lightValues[1]>thresholdValues[1]*1.05:
			GPIO.output(led2Pin, GPIO.LOW)
                        bike2Docked = False

		if lightValues[2]<thresholdValues[2] and bike3Docked == False:
			GPIO.output(led3Pin, GPIO.HIGH)
                        SaveToCloud()
                        bike3Docked = True
		elif lightValues[2]>thresholdValues[2]*1.05:
			GPIO.output(led3Pin, GPIO.LOW)
                        bike3Docked = False

		time.sleep(0.1) # this delay reduced the CPU utilisation from 100% to approx 50%
except KeyboardInterrupt:
	pass

GPIO.cleanup()
print("released GPIO")
time.sleep(2)
