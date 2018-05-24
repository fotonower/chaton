import cv2
import random
cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

limit=0
import sys
if len(sys.argv) >= 2:
   limit = int(sys.argv[1])

img_counter = 0



import sched, time
s = sched.scheduler(time.time, time.sleep)

def do_something(sc): 
    global img_counter, limit
    print ("Doing stuff...")
    # do your stuff

    ret, frame = cam.read()
#    cv2.imshow("test", frame)


    millis = int(round(time.time() * 1000))
    img_name = "/home/pi/workarea/opencv_frame_{}.png".format(millis)
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))
    img_counter = img_counter + 1
    print ("img_counter : " +str(img_counter) + "limit : " + str(limit))
    if limit != 0 and img_counter > limit :
        print("reach limit photo " + str(limit))
        exit(0)

    s.enter(0.1, 1, do_something, (sc,))

s.enter(0.1, 1, do_something, (s,))
s.run()







cam.release()

cv2.destroyAllWindows()
