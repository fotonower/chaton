from time import sleep
import RPi.GPIO as GPIO

import sys
import time
port = 11
nb_time = 1
wait_for = 10


if len(sys.argv) > 1:
    port = int(sys.argv[1])

if len(sys.argv) > 2:
    nb_time = int(sys.argv[2])

if len(sys.argv) > 3:
    wait_for = int(sys.argv[3])

def read_signal(port = 18, nb_time = 50, wait_for = 1):

	#init GPIO with BCM numberings
	GPIO.setmode(GPIO.BCM)
	#init every used pins
	GPIO.setup(port, GPIO.IN)#, pull_up_down=GPIO.PUD_DOWN)

        print (" port : " + str(port) + ", nb_time : " + str(nb_time) + ", wait_for : " + str(wait_for))

        ret = -1

        for i in range(nb_time):
            ret = GPIO.input(port)

            print(str(ret))

            if i > 0:
                time.sleep(wait_for)

        return ret

        GPIO.cleanup()

print(time.strftime("%c"))
read_signal(port, nb_time, wait_for)