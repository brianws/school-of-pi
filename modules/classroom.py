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
led1Pin = 22
led2Pin = 27
led3Pin = 17
button = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(led1Pin, GPIO.OUT)
GPIO.setup(led2Pin, GPIO.OUT)
GPIO.setup(led3Pin, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
        year_5_st_marys = 6
        sql = "INSERT INTO susschool_reading(type, amount, area_id, created_date) VALUES(%s, %s, %s, %s)"
        data = ('Bike', 1, year_5_st_marys, now)
        result = cursor.execute(sql, data)
        connection.commit()
        cursor.close()
        connection.close()


thresholdValues = [0,0,0] # parameter to store the trigger levels
hallValues = [0,0,0] #store the Hall effect sensor readings in an array
window1Open = False
window2Open = False
window3Open = False
cloudPublished = False


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

                # if the reset button is pressed, store the new light settings
                if not GPIO.input(button): #if the button is pressed
                        for i in range(3):
                                thresholdValues[i] = int(hallValues[i]*1.05) # 105% to introduce debounce


	# The threshold value is set at 105% above the calibated value.
	# When the sensor detects above the theshold value, it will change the led
	# To prevent flicker around the threshold point, add 5% to the threshold
	# when returning the led to the original state. If the value sits between
	# these two values, the led will simply retain its original state

		if hallValues[0]>thresholdValues[0] and window1Open == False:
			GPIO.output(led1Pin, GPIO.HIGH)
			window1Open = True
		elif hallValues[0]<thresholdValues[0]*1.05:
			GPIO.output(led1Pin, GPIO.LOW)
			window1Open = False
		if hallValues[1]>thresholdValues[1] and window2Open == False:
			GPIO.output(led2Pin, GPIO.HIGH)
			window2Open = True
		elif hallValues[1]<thresholdValues[1]*1.05:
			GPIO.output(led2Pin, GPIO.LOW)
			window2Open = False
		if hallValues[2]>thresholdValues[2] and window3Open == False:
			GPIO.output(led3Pin, GPIO.HIGH)
			window3Open = True
		elif hallValues[2]<thresholdValues[2]*1.05:
			GPIO.output(led3Pin, GPIO.LOW)
			window3Open = False

		if (window1Open == True or window2Open == True or window3Open == True) and cloudPublished == False:
			SaveToCloud()
			cloudPublished = True

                if window1Open == False and window2Open == False and window3Open == False:
                        cloudPublished = False

                print "W1?", window1Open, "W2?", window2Open, "W3?", window3Open, "Published?", cloudPublished


		time.sleep(0.1) # this delay reduced the CPU utilisation from 100% to approx 50%
except KeyboardInterrupt:
	pass
	
GPIO.cleanup()
print("released GPIO")
time.sleep(2)
