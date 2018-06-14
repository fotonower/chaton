from picamera import PiCamera
from datetime import datetime
camera = PiCamera()
import os
from time import sleep
camera.start_preview()
camera.rotation = 180
folder = ""
last_hour = ""
while True:
    now = datetime.now()
    day = now.strftime("%d%m%Y")
    hour = now.strftime("%H")
    minutes = now.strftime("%M")
    if last_hour != hour:
        folder = '/home/pi/Desktop/images/%s/%s/%s' % day,hour,minutes
        os.makedirs(folder)
    camera.capture(folder + '/image%s.jpg' % now.strftime("%S"))
    sleep(1)
