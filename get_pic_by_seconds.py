from picamera import PiCamera
from datetime import datetime
camera = PiCamera()
import os, sys
from time import sleep
camera.start_preview()
camera.rotation = 180
folder = ""
last_hour = ""

while True:
    sys.stdout.write(".")
    sys.stdout.flush()
    now = datetime.now()
#    now_date = str(now).replace(":", "_").replace(" ", "").replace("-", "_").replace(".", "_").replace("\/", "_")
#    print(now_date)
    day = now.strftime("%d%m%Y")
    hour = now.strftime("%H")
    minutes = now.strftime("%M")
    if last_hour != hour:
        folder = '/home/pi/Desktop/images' + str(day) + "/" + str(hour) + "/" + str(minutes)
        if not os.path.exists(folder):
            os.makedirs(folder)

    camera.capture(folder + '/image' + str(now.strftime("%S.%f")) + ".jpg")
#    camera.capture(os.path.join(folder, "image_" + str(now_date) + ".jpg"))
    sleep(0.1)
