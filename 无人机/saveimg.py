#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
# import ffmpeg
import time
import cv2
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np

if __name__ == '__main__':
    rospy.init_node('doimg')
    rtsp_url ="rtsp://127.0.0.1:8554/live"
    frame_count = 0
    # save_interval = 5
    saved_frame_count = 0
    # start_time = 0
    
    while(1):        
        # while cap.isOpened():
        current_time=time.time()
        cap = cv2.VideoCapture(rtsp_url)
        ret, frame = cap.read()
        # cv2.imshow("test",frame)
        # frame_count += 1
        # if(frame_count >= 100):
        
        frame_count=0
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # # time.sleep(0.5)
        barcode = pyzbar.decode(gray)
        if(barcode!=[]):
            # print(barcode)
        # else:
            print(barcode[0])

        # if current_time - start_time > save_interval :
        # # if barcode !=[] :

        file_name='/root/tta_ros/img/{}.jpg'.format(saved_frame_count)
        cv2.imwrite(file_name,frame)
        saved_frame_count+=1
            # start_time=current_time
        print(time.time()-current_time)
    cap.release()
        
