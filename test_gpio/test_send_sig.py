#!/usr/bin/python
import RPi.GPIO as gpio
import time

# on passe en mode BMC qui veut dire que nous allons utiliser directement
# le numero GPIO plutot que la position physique sur la carte
gpio.setmode(gpio.BCM)

# defini le port GPIO 4 comme etant une sortie output
gpio.setup(17, gpio.OUT)

# Mise a 1 une seconde puis 0 une seconde
while True:
   gpio.output(17, gpio.LOW)
   print("signal sent")
   time.sleep(5)
   gpio.output(17, gpio.HIGH)
   print("signal stop")
   time.sleep(5)