'''
Created on Mar 17, 2017
@author: Wonhee Cho
email : danylight@gmail.com
Web site: http://mediaq.usc.edu/mmsys17
Copyright 2017 Wonhee Cho
Function: Generate Photo
'''
import os
from PIL import Image
import cv2

def gen_photo(output_filepath_movie,output_filepath_temp):
    print(" photo image ")
    vidcap = cv2.VideoCapture(output_filepath_movie)
    check,image = vidcap.read()
    if check:
        check,image = vidcap.read()
        cv2.imwrite(output_filepath_temp, image)     # save frame as JPEG file
    else:
        print("-----> failed to save photo")

    return check
