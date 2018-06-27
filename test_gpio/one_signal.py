
from time import sleep
import RPi.GPIO as GPIO
from picamera import PiCamera
from picamera.array import PiRGBArray
#from keras.models import load_model
import numpy as np
#####################################


import sys
import time
port = 23
pulse = 46
signal = 7
duration = 2

if len(sys.argv) > 1:
    port = int(sys.argv[1])
if len(sys.argv) > 2:
    pulse = int(sys.argv[2])
if len(sys.argv) > 3:
    signal = float(sys.argv[3])
if len(sys.argv) > 4:
    duration = float(sys.argv[4])

def send_signal(port = 23, pulse = 46, signal = 7., duration = 1.) :

	#init GPIO with BCM numberings
	GPIO.setmode(GPIO.BCM)
	#init every used pins
	GPIO.setup(port, GPIO.OUT)


	#set controls
	CONTROLLER = GPIO.PWM(port, pulse)

	CONTROLLER.start(0)
	CONTROLLER.ChangeDutyCycle(signal)

        print (" port :  " + str(port) + ", pulse : " + str(pulse) + ", signal : " + str(signal) + " , duration : " + str(duration))

        time.sleep(duration)

	CONTROLLER.stop(0)

	print("STOP")

	GPIO.cleanup()
        return




send_signal(port, pulse, signal, duration) 
