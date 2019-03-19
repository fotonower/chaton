
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

def dump_photo_taken(to_dump):
    print(to_dump)
    test = 1


def take_pictures(lsr,base_folder,end,pause,shutter,quality,verbose= False,width=720,height=480):

    camera = ""
    try:
        camera = PiCamera()
        camera.resolution = (width, height)
        camera.rotation = x.rotation % 360
        camera.shutter_speed = shutter
        print("launching script")
    except Exception, e:
        print("camera allready in use")
        return
    folder = ""
    last_minute = ""
    photo_taken_by_hour = 0
    now = datetime.now()
    last_hour =  now.strftime("%H")
    while True:
        if verbose:
            print("taking picture")
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
        now = datetime.now()
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
        camera.capture(filename, quality=quality,thumbnail=None)
        if hour != last_hour:
            dump_photo_taken(photo_taken_by_hour)
            photo_taken_by_hour = 0
            last_hour = hour
        photo_taken_by_hour += 1
        lsr.append_photo(filename)
        sleep(pause)


def test(rotation,gpio_pin,gpio_pin2,shutter,folder,verbose,width=720,height=480,delay=60,fs=44100):
    import RPi.GPIO as GPIO
    import time
    camera = ""
    try:
        camera = PiCamera()
        camera.resolution = (width,height)
        #camera.start_preview()
        camera.rotation = rotation % 360
        camera.shutter_speed = shutter
        print("launching script")
    except Exception, e:
        print("camera allready in use")
        exit(0)
    if gpio_pin == gpio_pin2:
        print("ERROR : gpio_pin HALL = gpio_pin LIGHT ")
        exit(0)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_pin2, GPIO.OUT)
    while True:
        GPIO.output(gpio_pin2, GPIO.LOW)
        for i in range(0,50):
            time.sleep(0.10)
            take_picture(lsr, folder, camera, verbose)
        GPIO.output(gpio_pin2, GPIO.HIGH)
        time.sleep(delay)

def get_sensor_and_take_pic(rotation,gpio_pin,gpio_pin2,shutter,folder,verbose,width=720,height=480,duration=60,fs=44100):
    import RPi.GPIO as GPIO

    camera = ""
    try:
        camera = PiCamera()
        camera.resolution = (width, height)
        camera.rotation = rotation % 360
        camera.shutter_speed = shutter
        print("launching script")
    except Exception, e:
        print("camera allready in use")
        exit(0)
    if gpio_pin == gpio_pin2:
        print("ERROR : gpio_pin HALL = gpio_pin LIGHT ")
        exit(0)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_pin, GPIO.IN)
    if gpio_pin2 != 0 :
        GPIO.setup(gpio_pin2, GPIO.OUT)

    while True:
        ret = GPIO.input(gpio_pin)
        if int(ret) == 1:
            if gpio_pin2 != 0:
                GPIO.output(gpio_pin2, GPIO.LOW)
            take_picture(lsr, folder, camera, verbose)
        else:
            if gpio_pin2 != 0:
                GPIO.output(gpio_pin2, GPIO.HIGH)

def get_sensor_card_and_take_pic(rotation,gpio_pin,shutter,folder,verbose,width=720,height=480):
    import ads1256  # import this lib
    ads1256.start(str(1), "25")
    camera = ""
    try:
        camera = PiCamera()
        camera.resolution = (width, height)
        camera.rotation = rotation % 360
        camera.shutter_speed = shutter
        print("launching script")
    except Exception, e:
        print("camera allready in use")
        exit(0)
    while True:
        ret = ads1256.read_channel(gpio_pin)
        if int(ret) > 4000000:
            take_picture(lsr, folder, camera, verbose)

def get_sound(base_folder,duration,fs,verbose):
    try:
        import sounddevice as sd
        from scipy.io.wavfile import write
    except Exception, e:
        print("lib not installed")
        exit(1)
    while True:
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        now = datetime.now()
        day = now.strftime("%d%m%Y")
        hour = now.strftime("%H")
        minutes = now.strftime("%M")
        folder = os.path.join(base_folder, '{}/{}/{}'.format(str(day), str(hour), str(minutes)))
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = folder + '/sound_{}_{}_{}_{}_{}.wav'.format(str(day), str(hour), str(minutes), now.strftime("%S"),
                                                               now.microsecond)
        if verbose:
            print("dumping sound into {}".format(filename))
        write(filename, fs, myrecording)


def test_connect(root_url, verbose= False):
    import socket
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(root_url)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False

if __name__ == "__main__":
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
                          default="take_photo", help="job : take_photo(default), take_photo_from_captor,get_sound,(to integrate here :) upload, upload_error, stat")
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
    parser.add_option('-G', '--gpiopin', type='int',dest='gpio_pin', default=17, help="gpio pin for HALL EFFECT captor")
    parser.add_option('-H', '--gpiopin2', type='int',dest='gpio_pin2', default=0, help="gpio pin for LIGHT captor")
    parser.add_option('-s','--shutter_speed',dest='shutter',default=10000,type='int',help='shutter speed for camera',action='store')
    parser.add_option('-q', '--quality', dest='quality', default=100, type='int', help='compression quality for jpeg format')
    parser.add_option('-w', '--width', dest='width', default=720, type='int',help='width of picture')
    parser.add_option('--height', dest='height', default=480, type='int',help='height of picture')
    parser.add_option('--duration', dest='duration',default=60,type='int',help='duration for sound recording')
    parser.add_option('--fs',dest='fs',default=44100,type='int',help='sound frequency')
    parser.add_option('-m', '--media', action='store_true', default=False, dest='media',
                        help='if true images to upload on external device')
    (x, args) = parser.parse_args()

    folder_local_db = x.folder_local_db
    file_local_db = x.file_local_db
    job = x.job

    lsr = LSR(file_local_db, folder_local_db)
    folder = x.folder
    if x.media:
        list_medias = os.listdir("/media/pi")
        if len(list_medias) > 0:
            print("taking first media in {}").format(list_medias[0])
            temp = os.path.join("/media/pi",list_medias[0])
            folder = os.path.join(temp,"images")
            try:
                os.makedirs(folder)
            except Exception, e:
                pass

    if job == "take_photo": # VR 29-8-18 : I suggest to make a function of all this instead of having it in the main
            take_pictures(lsr,folder, x.end, x.pause,x.shutter,x.quality, x.verbose, x.width,x.height)
    elif job == 'take_photo_from_captor':
        get_sensor_and_take_pic(x.rotation, x.gpio_pin,x.gpio_pin2, x.shutter, folder, x.verbose, x.duration, x.width,x.height)
    elif job == 'take_photo_from_card':
        get_sensor_card_and_take_pic(x.rotation, x.gpio_pin, x.shutter, folder, x.verbose, x.width,x.height)
    elif job == 'get_sound':
        get_sound(folder,x.duration,x.fs,x.verbose)
    elif job == 'test':
        test(x.rotation, x.gpio_pin,x.gpio_pin2, x.shutter, folder, x.verbose, x.duration, x.width,x.height)
    elif job == "test_connect":
        is_connected = test_connect(x.root_url, x.verbose)
        print("is connected = {}".format(is_connected))
    else :
        print ("Job " + str(job) + " not yet implemented !")


