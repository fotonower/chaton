#bingogogog
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""


def cameraGetPic():
    print("cameraGetPic")

def cameraRecordVideo():
    print("cameraRecordVideo")


while True:
    try:
        print("\n1 - Start get picture ")
        print("2 - Start record video ")
        print("3 - Exit \n")
        user_input = int(raw_input("Please enter your choice (1) - (2) - (3) : "))
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
        continue
    else:
        if(user_input > 3):
            continue
        else:
            #we're ready to exit the loop.
            break

if user_input == 1: 
    cameraGetPic()
if user_input == 2:
    cameraRecordVideo()
if user_input == 3:
    print("Good bye ! ")
    exit()
