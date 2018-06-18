from picamera import PiCamera
from datetime import datetime
camera = PiCamera()
import os
from time import sleep
camera.start_preview()
camera.rotation = 180
folder = ""
last_minute = ""
while True:
    now = datetime.now()
    day = now.strftime("%d%m%Y")
    hour = now.strftime("%H")
    minutes = now.strftime("%M")
    if int(hour) >= 22:
        exit(0)
    if last_minute != minutes:
        folder = '/home/pi/Desktop/images/{}/{}/{}'.format(str(day),str(hour),str(minutes))
        os.makedirs(folder)
	last_minute = minutes
    camera.capture(folder + '/image%s.jpg' % now.strftime("%S"))
    sleep(1)
