
from datetime import datetime
import os, sys
from time import sleep
from picamera import PiCamera
from lib.local_stat_raspberry import LocalStatRaspberry as LSR

from optparse import OptionParser

def take_picture(lsr,base_folder,camera,verbose=False):
    if verbose:
        print("taking picture")
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
    now = datetime.now()
    day = now.strftime("%d%m%Y")
    hour = now.strftime("%H")
    minutes = now.strftime("%M")
    folder = os.path.join(base_folder, '{}/{}/{}'.format(str(day), str(hour), str(minutes)))
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = folder + '/image_{}_{}_{}_{}_{}.jpg'.format(str(day), str(hour), str(minutes), now.strftime("%S"),
                                                           now.microsecond)
    camera.capture(filename)
    if lsr:
        lsr.append_photo(filename)

def take_pictures(lsr,base_folder,end,pause,shutter,verbose= False):

    camera = ""
    try:
        camera = PiCamera()
        camera.start_preview()
        camera.rotation = x.rotation % 360
        camera.shutter_speed = shutter
        print("launching script")
    except Exception, e:
        print("camera allready in use")
        return
    folder = ""
    last_minute = ""
    while True:
        if verbose:
            print("taking picture")
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
        now = datetime.now()
        #    now_date = str(now).replace(":", "_").replace(" ", "").replace("-", "_").replace(".", "_").replace("\/", "_")
        #    print(now_date)
        day = now.strftime("%d%m%Y")
        hour = now.strftime("%H")
        minutes = now.strftime("%M")

        if int(hour) >= end:
            exit(0)
        if last_minute != minutes:
            folder = os.path.join(base_folder, '{}/{}/{}'.format(str(day), str(hour), str(minutes)))
            if not os.path.exists(folder):
                os.makedirs(folder)
        last_minute = minutes
        filename = folder + '/image_{}_{}_{}_{}_{}.jpg'.format(str(day), str(hour), str(minutes), now.strftime("%S"), now.microsecond)
        camera.capture(filename)
        lsr.append_photo(filename)
        sleep(pause)

def get_sensor_and_take_pic(rotation,gpio_pin,shutter,folder,verbose):
    import RPi.GPIO as GPIO
    camera = ""
    try:
        camera = PiCamera()
        camera.start_preview()
        camera.rotation = rotation % 360
        camera.shutter_speed = shutter
        print("launching script")
    except Exception, e:
        print("camera allready in use")
        exit(0)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_pin, GPIO.IN)
    while True:
        ret = GPIO.input(gpio_pin)
        if int(ret) == 0:
            take_picture(lsr, folder, camera, verbose)

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

parser.add_option("-j", "--job", action="store", type="string", dest="job",
                      default="take_photo", help="job : take_photo(default), take_photo_from_captor,(to integrate here :) upload, upload_error, stat")

parser.add_option("--folder_local_db", action="store", type="string", dest="folder_local_db", default="/home/pi/.fotonower_config",
                      help="local folder to save stat and info")
parser.add_option("--file_local_db", action="store", type="string", dest="file_local_db", default="/home/pi/.fotonower_config/sqlite.db",
                      help="local file to save stat and info in sqlite format")


parser.add_option("-t", "--token", action="store", type="string", dest="token",
                      default="empty_dummy", help=" token ")

parser.add_option("-u", "--root_url", action="store", type="string", dest="root_url", default="vision.fotonower.com",
                      help="root_url to upload photos")

parser.add_option("-d", "--datou", action="store", type="string", dest="datou",
                      default="2",help="datou id to be treated")
parser.add_option("-P", "--protocol", action="store", type="string", dest="protocol",
                      default="https", help="http or https")
parser.add_option("-D", "--day", type='string', dest='day', default="", help="day of folder to upload")
parser.add_option('-G', '--gpiopin', type='int',dest='gpio_pin', default=17, help="gpio pin for captor to test")
parser.add_option('-s','--shutter_speed',dest='shutter',default=10000,type='int',help='shutter speed for camera',action='store')
(x, args) = parser.parse_args()

folder_local_db = x.folder_local_db
file_local_db = x.file_local_db
job = x.job

lsr = LSR(file_local_db, folder_local_db)

if job == "take_photo": # VR 29-8-18 : I suggest to make a function of all this instead of having it in the main
    take_pictures(lsr,x.folder, x.end, x.pause,x.shutter, x.verbose)
elif job == 'take_photo_from_captor':
    get_sensor_and_take_pic(x.rotation, x.gpio_pin, x.shutter, x.folder, x.verbose)
else :
    print ("Job " + str(job) + " not yet implemented !")


