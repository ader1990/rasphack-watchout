import os
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

while True:
    GPIO.output(23, GPIO.HIGH)
    print ('HallHigh')
    time.sleep(2)
    print ('HallLow')
    time.sleep(2)

