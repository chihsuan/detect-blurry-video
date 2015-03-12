#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import sys

import cv2
import cv2.cv as cv
from detect_blurry_image import detect_blurry_image

def detect_blurry(video_path):
    print 'video:', video_path

    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print "Error, could not open the video", video_name
        sys.exit(1)

    pos_frame = 0
    total_frames = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    number_of_blur = 0
    while pos_frame < total_frames:
        video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame)
        flag, img = video.read()
        
        # gray is good for image processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        if detect_blurry_image(gray, MinZero=0.025):
            number_of_blur += 1

        pos_frame += 24

    video.release()
    if number_of_blur >= (total_frames/24*0.5):
        print 'A blurry video'
    else:
        print 'Not a blurry video'


if __name__=='__main__':
    # video path
    detect_blurry(sys.argv[1])
