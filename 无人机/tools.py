#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from ttauav_node.srv import *
from time import sleep
import cv2
import os
import csv
import io
import pyzbar.pyzbar as pyzbar
import numpy as np
# import pandas as pd

def do_takeoff_or_landing(torlmsg):
    rospy.init_node('client')
    rospy.wait_for_service('takeoffOrLanding')
    try:
        takeoff_landing = rospy.ServiceProxy('takeoffOrLanding', takeoffOrLanding)
        response = takeoff_landing.call(torlmsg)
        if response:
            rospy.loginfo("Do takeoff or landing success!!!!!")
            rospy.loginfo("Result: %d", response.ack)
        else:
            rospy.loginfo("Do takeoff or landing failed!!")
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed: %s", e)
    sleep(6)

def pos_controlnd(Yaw, vel_n, vel_e, vel_d, fly_time):
    rospy.init_node('client')
    rospy.wait_for_service('flightByVel')
    try:

        flight_vel = flightByVelRequest()
        flight_vel.targetYaw=Yaw
        flight_vel.vel_n=vel_n
        flight_vel.vel_e=vel_e
        flight_vel.vel_d=vel_d
        flight_vel.fly_time=fly_time

        client = rospy.ServiceProxy('flightByVel', flightByVel)
        response = client.call(flight_vel)

        if response:
            rospy.loginfo("Control success!!!!!")
            rospy.loginfo("Result: %d", response.ack)
        else:
            rospy.loginfo("Control failed!!!!!!")
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed: %s", e)

def pos_control(Yaw, vel_n, vel_e, vel_d, fly_time):
    rospy.init_node('client')
    rospy.wait_for_service('flightByVel')
    try:

        flight_vel = flightByVelRequest()
        flight_vel.targetYaw=Yaw
        flight_vel.vel_n=vel_n
        flight_vel.vel_e=vel_e
        flight_vel.vel_d=vel_d
        flight_vel.fly_time=fly_time

        client = rospy.ServiceProxy('flightByVel', flightByVel)
        response = client.call(flight_vel)

        if response:
            rospy.loginfo("Control success!!!!!")
            rospy.loginfo("Result: %d", response.ack)
        else:
            rospy.loginfo("Control failed!!!!!!")
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed: %s", e)
    sleep(fly_time/1000)

def yuntai_control(pos):
    rospy.init_node('client')
    rospy.wait_for_service('gimbalControl')
    try:
        gimbalmsg = gimbalControlRequest()
        client = rospy.ServiceProxy('gimbalControl', gimbalControl)
        gimbalmsg.pitch=pos
        gimbalmsg.roll=0
        gimbalmsg.yaw=0
        response = client.call(gimbalmsg)
        if response:
            rospy.loginfo("gimbalchange success!!!!!")
            rospy.loginfo("Result: %d", response.ack)
        else:
            rospy.loginfo("Control failed!!!!!!")
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed: %s", e)
    sleep(1)

saved_frame_count = 0

def save_to_csv(data):
    # 打开CSV文件，检查是否已经存在该行数据
    # with open('data.csv', 'r') as csvfile:
    #     reader = csv.reader(csvfile)
    #     for row in reader:
    #         if data in row:
    #             return  # 如果数据已存在则直接返回

    # 如果数据不存在，将数据写入CSV文件
    with open('data.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data])

def paizhao():

    global saved_frame_count

    rtsp_url ="rtsp://127.0.0.1:8554/live"
    cap = cv2.VideoCapture(rtsp_url)

    ret, frame = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        rospy.loginfo("Something Wrong in Img!!!")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)
    if(barcodes != []):
        for barcode in barcodes:
            # 提取二维码内容
            data = barcode.data.decode("utf-8")
            print(data)
            # 将结果保存到CSV文件
            save_to_csv(data)
            
    
    # file_name='/mnt/img/{}.jpg'.format(saved_frame_count)
    # cv2.imwrite(file_name,frame)

    saved_frame_count+=1

flag = 1

movelist=[[0,0,0.2,0,1000],[0,0.2,0,0,2000],[0,0,-0.2,0,2000],[0,-0.2,0,0,2000]]

def do_land():
    
    rtsp_url = "rtsp://127.0.0.1:8554/live"
    cap = cv2.VideoCapture(rtsp_url)
    sleep_time = 2
    max_attempts = 4
    global flag
    flag = True

    def read_frame():
        rtsp_url = "rtsp://127.0.0.1:8554/live"
        cap = cv2.VideoCapture(rtsp_url)
        _, frame = cap.read()
        # frame = cv2.imread('1.jpg')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcode = pyzbar.decode(gray)
        return barcode, frame
    
    def adjust_position(x, y, w, h):
        global flag
        wrong = 0

        while w <= 500 or x <= 600 or x >= 1200 or y <= 200 or y >= 500:
            xdir, ydir, wdir = 0.0, 0.0, 0.0
            rospy.loginfo("x: {}, y: {}, w: {}, h: {}".format(x, y, w, h))

            if(w <= 200):
                if x <= 300: #871.5 340.5 663 669
                    rospy.loginfo("Left!")
                    xdir = -0.2
                elif x <= 600:
                    rospy.loginfo("Left!")
                    xdir = -0.1
                elif x >= 1300:
                    rospy.loginfo("Right!")
                    xdir = 0.2
                elif x >= 1000:
                    rospy.loginfo("Right!")
                    xdir = 0.1
                
                if y <= 50:
                    rospy.loginfo("Forward!")
                    ydir = 0.2
                elif y <= 250:
                    rospy.loginfo("Forward!")
                    ydir = 0.1
                elif y >= 550:
                    rospy.loginfo("Back!")
                    ydir = -0.2
                elif y >= 420:
                    rospy.loginfo("Back!")
                    ydir = -0.1 

                if xdir == 0.0 and ydir == 0.0:
                    wdir = -0.4
                else:
                    wdir = -0.2
                
                rospy.loginfo("111")
                pos_controlnd(0, ydir, xdir, 0, 2000)
                sleep(2)

                pos_controlnd(0, 0, 0, wdir, 2000)
                sleep(2)

            else:

                if x <= 300: #871.5 340.5 663 669
                    rospy.loginfo("Left!")
                    xdir = -0.1
                elif x <= 600:
                    rospy.loginfo("Left!")
                    xdir = -0.05
                elif x >= 1300:
                    rospy.loginfo("Right!")
                    xdir = 0.1
                elif x >= 1000:
                    rospy.loginfo("Right!")
                    xdir = 0.05

                if y <= 50:
                    rospy.loginfo("Forward!")
                    ydir = 0.1
                elif y <= 250:
                    rospy.loginfo("Forward!")
                    ydir = 0.05
                elif y >= 550:
                    rospy.loginfo("Back!")
                    ydir = -0.1
                elif y >= 420:
                    rospy.loginfo("Back!")
                    ydir = -0.05

                if xdir == 0.0 and ydir == 0.0:
                    wdir = -0.4
                else:
                    wdir = -0.2

                rospy.loginfo("222")

                pos_controlnd(0, ydir, xdir, 0, 1000)
                sleep(1)

                pos_controlnd(0, 0, 0, wdir, 1000)
                sleep(1)

            barcode, _ = read_frame()
            sleep(2)
            if  barcode == []:
                wrong += 1
                rospy.loginfo("Something went wrong!")
                ydir = -ydir
                xdir = -xdir
                wdir = -wdir
                pos_controlnd(0, ydir, xdir, wdir, 1000)
                sleep(1)

                if wrong == max_attempts:
                    do_takeoff_or_landing(2)
            else:
                wrong = 0
                (x, y, w, h) = barcode[0].rect
                x = x + w / 2.0
                y = y + h / 2.0

        do_takeoff_or_landing(2)


    barcode, _ = read_frame()
    if  barcode==[]:
        rospy.loginfo("QR code not found!")
        for i in range(0,4):
            barcode, frame = read_frame()
            
            if barcode:
                break
            else:
                rospy.loginfo("Does not detect!")
                pos_controlnd(movelist[i])  # Move around
                sleep(sleep_time)
                cap = cv2.VideoCapture(rtsp_url)
                sleep(sleep_time)
            if(i==3):
                flag = False

    if flag:
        (x, y, w, h) = barcode[0].rect
        x = x + w / 2.0
        y = y + h / 2.0
        if barcode:
            adjust_position(x, y, w, h)
    else:
        rospy.loginfo("QR code not found!")

    # if(barcode==[]):
    #     rospy.loginfo("Does not detect!!!")
    #     pos_controlnd(0, 0, 0.2, 0, 1000) #向右
    #     sleep(2)
    #     cap = cv2.VideoCapture(rtsp_url)
    #     ret, frame = cap.read()
    #     sleep(2)
    #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #     barcode = pyzbar.decode(gray)
    #     if(barcode==[]):
    #         pos_controlnd(0, 0.2, 0, 0, 1000) #向上
    #         sleep(2)
    #         cap = cv2.VideoCapture(rtsp_url)
    #         ret, frame = cap.read()
    #         sleep(2)
    #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #         barcode = pyzbar.decode(gray)
    #         if(barcode==[]):
    #             pos_controlnd(0, 0,-0.2, 0, 2000) #向左
    #             sleep(2)
    #             cap = cv2.VideoCapture(rtsp_url)
    #             ret, frame = cap.read()
    #             sleep(2)
    #             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #             barcode = pyzbar.decode(gray)
    #             if(barcode==[]):
    #                 pos_controlnd(0, -0.2, 0, 0, 2000) #向后
    #                 sleep(2)
    #                 cap = cv2.VideoCapture(rtsp_url)
    #                 ret, frame = cap.read()
    #                 sleep(2)
    #                 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #                 barcode = pyzbar.decode(gray)
    #                 if(barcode==[]):
    #                     pos_controlnd(0, 0, 0.2, 0, 2000) #向右
    #                     sleep(2)
    #                     cap = cv2.VideoCapture(rtsp_url)
    #                     ret, frame = cap.read()
    #                     sleep(2)
    #                     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #                     barcode = pyzbar.decode(gray)
    #                     if(barcode==[]):
    #                         flag=0
    # if(flag):
    #     (x, y, w, h) = barcode[0].rect
    #     x=x+w/2.0
    #     y=y+h/2.0  #871.5 340.5 663 669
    #     wrong=0
    #     while(w<=500 or h<=500 or w>=1000 or h<=1000 or x<=600 or x>=1200 or y<=250 or y>=500 ):
    #         xdir=0.0
    #         ydir=0.0
    #         wdir=0.0
    #         rospy.loginfo("x:{},y:{},w:{},h:{}".format(x,y,w,h))
    #         if x<=300:
    #             rospy.loginfo("Left!!!")
    #             xdir=-0.1
    #         elif x<=600:
    #             rospy.loginfo("Left!!!")
    #             xdir=-0.05
    #         elif x>=1300:
    #             rospy.loginfo("Right!!!")
    #             xdir=0.1
    #         elif x>=1000:
    #             rospy.loginfo("Right!!!")
    #             xdir=0.05
    #         if y<=50:
    #             rospy.loginfo("foward!!!")
    #             ydir=0.1
    #         elif y<=250:
    #             rospy.loginfo("foward!!!")
    #             ydir=0.05
    #         elif y>=550:
    #             rospy.loginfo("back!!!")
    #             ydir=-0.1
    #         elif y>=420:
    #             rospy.loginfo("back!!!")
    #             ydir=-0.05
    #         if w<=200:
    #             if xdir==0.0 and ydir ==0.0:
    #                 wdir = -0.6
    #             else:
    #                 wdir=-0.3
    #         elif w<=500:
    #             wdir=-0.05
            
    #         pos_controlnd(0,ydir,xdir,wdir,1000)
    #         sleep(1)

    #         cap = cv2.VideoCapture(rtsp_url)
    #         ret, frame = cap.read()
    #         sleep(2)
    #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #         barcode = pyzbar.decode(gray)
    #         if(barcode==[]):
    #             wrong +=1
    #             rospy.loginfo("Something Wrong!!!")
    #             ydir=-ydir
    #             xdir=-xdir
    #             pos_controlnd(0,ydir,xdir,wdir,1000)
    #             sleep(1)
    #             if(wrong==4):
    #                 do_takeoff_or_landing(2)

    #         else:
    #             wrong=0
    #             (x, y, w, h) = barcode[0].rect
    #             x=x+w/2.0
    #             y=y+h/2.0  #871.5 340.5 663 669
    #     do_takeoff_or_landing(2)
    # else:
    #     rospy.loginfo("QRcode not found!!")
    
            

