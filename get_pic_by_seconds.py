from picamera import PiCamera
from datetime import datetime
import os, sys
from time import sleep

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--folder", action="store", type="string", dest="folder", default="/home/pi/Desktop/images",
                      help="base folder where photos are saved")
parser.add_option("-p", "--pause", action="store", type="float", dest="pause",
                      default=1.0, help="interval between photos")
parser.add_option("-r", "--rotation", action="store", type="int", dest="rotation",
                      default=180, help="rotation of photos")
parser.add_option("-e", "--end", action="store", type="int", dest="end",
                      default=22, help="rotation of photos")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=0, help=" verbose ")

(x, args) = parser.parse_args()

camera = ""
try :
    camera = PiCamera()
    camera.start_preview()
    camera.rotation = x.rotation % 360
    camera.resolution = (1280, 720)
    camera.resolution = (2592, 1944)
    camera.shutter_speed = 10000
    print("launching script")
except Exception, e:
    print("script allready launched")
    print (str(e))
    exit(0)
folder = ""
last_hour = ""
last_minute = ""
while True:
    if x.verbose:
        sys.stdout.write(".")
        sys.stdout.flush()
    now = datetime.now()
#    now_date = str(now).replace(":", "_").replace(" ", "").replace("-", "_").replace(".", "_").replace("\/", "_")
#    print(now_date)
    day = now.strftime("%d%m%Y")
    hour = now.strftime("%H")
    minutes = now.strftime("%M")
    if int(hour) >= x.end:
        exit(0)
    if last_minute != minutes:
        folder = os.path.join(x.folder,'{}/{}/{}'.format(str(day),str(hour),str(minutes)))
        if not os.path.exists(folder):
            os.makedirs(folder)
	last_minute = minutes
    camera.capture(folder + '/image_{}_{}_{}_{}.jpg'.format(str(day),str(hour),str(minutes),now.strftime("%S")))
    sleep(x.pause)

