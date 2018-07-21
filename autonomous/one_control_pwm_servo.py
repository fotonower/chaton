
from time import sleep
import RPi.GPIO as GPIO
from picamera import PiCamera
from picamera.array import PiRGBArray
#from keras.models import load_model
import numpy as np
#####################################


import sys
import time
port = 1
pulse = 60
signal = 10
duration = 2

if len(sys.argv) > 1:
    port = int(sys.argv[1])
if len(sys.argv) > 2:
    pulse = int(sys.argv[2])
if len(sys.argv) > 3:
    signal = float(sys.argv[3])
if len(sys.argv) > 4:
    duration = float(sys.argv[4])

def send_signal(port = 23, pulse = 46, value = 7., duration = 1., verbose = True) :


        try:
			from Adafruit_PCA9685 import PCA9685

			pwm = PCA9685()
			pwm.set_pwm_freq(60)
        except Exception as e:
			print('The car will not be able to move')
			print('Are you executing this code on your laptop?')
			print('The adafruit error: ', e)
			pwm = None

        print (" port :  " + str(port) + ", pulse : " + str(pulse) + ", signal : " + str(signal) + " , duration : " + str(duration))


	if pwm is not None:
			pwm.set_pwm(port, 0 , int(value))
			if verbose:
				print('GAS : ', value)
	else:
			if verbose:
				print('PWM module not loaded')


        time.sleep(duration)


	print("STOP")

        return




send_signal(port, pulse, signal, duration) 



