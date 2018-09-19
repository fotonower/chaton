#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from skimage.measure import compare_ssim as ssim
#import matplotlib.pyplot as plt
import numpy as np
import cv2
from lib.local_stat_raspberry import LocalStatRaspberry as LSR



def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def compare_images(imageA, imageB, title):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)


def get_image_and_compare(lsr,limit, threshold,verbose = False):
    images = lsr.get_photo_to_treat(limit)
    to_update = []
    to_delete = []
    picA = []
    picB = []
    for i in range(1,len(images)):
        if len(picA) == 0 :
            picA = cv2.imread(images[i-1][3])
        picB = cv2.imread(images[i][3])
        m = mse(picA, picB)
        s = ssim(picA, picB)
        picA = picB

        if m < threshold:
            tmp = images[i-1][3].split('.')
            new_name = tmp[0]+'_to_delete.' + tmp[2]
            #a modifier par un delete quand on aura confirmer que les photos etaient bien a supprimer
            os.rename(images[i-1][3], new_name)
            to_delete.append({"id":str(images[i-1][0]),"filename" : new_name, "to_upload" : "-1"})
            #a supprimer quand on aura confirmer que les photos etaient bien a supprimer
            to_update.append(str(images[i - 1][0]))
        else:
            to_update.append(str(images[i-1][0]))
    if len(to_delete) > 0:
        for item in to_delete:
            lsr.update_one(item['id'], ["filename","to_upload"],[item['filename'],item['to_upload']])


    lsr.set_pic_to_upload(to_update)


    test = 1


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='image checker for rapsberry')
    parser.add_argument("--folder_local_db", action="store", type=str, dest="folder_local_db",
                        default="/home/pi/.fotonower_config",
                        help="local folder to save stat and info")
    parser.add_argument("--file_local_db", action="store", type=str, dest="file_local_db",
                        default="/home/pi/.fotonower_config/sqlite.db",
                        help="local file to save stat and info in sqlite format")
    parser.add_argument('-l',"--limit", action="store", type=int, dest="limit",
                        default=10,
                        help="limit picture treatment")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=0, help=" verbose ")
    parser.add_argument("-t", "--threshold", action="store", dest="threshold", default=0.01, help=" verbose ")
    parser.add_argument('-j', '--job', dest="job", type=str, action="store", default="compare", help="only compare job atm, more jobs to come")
    x = parser.parse_args()

    folder_local_db = x.folder_local_db
    file_local_db = x.file_local_db
    lsr = None
    try:
        lsr = LSR(file_local_db, folder_local_db)
    except:
        print("no sqlite3 installed")

    if x.job == "compare":
        get_image_and_compare(lsr,x.limit,x.threshold,x.verbose)
