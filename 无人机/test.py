#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from ttauav_node.srv import *
from time import sleep
import cv2
from arm import *

def test():
    rospy.loginfo("Down!")
    pos_control(0, 0, 0, -0.5, 1000)  # 下降

    yuntai_control(-90)
    rospy.loginfo("yuntai change -90! Now -90!!")

def first():
    
    pos_control(0, 0, 0.3, 0, 4300)  # 向右
    rospy.loginfo("Right1!")

    paizhao()

    pos_control(0, 0, 0.3, 0, 2000)  # 向右
    rospy.loginfo("Right2!")

    paizhao()
    
    pos_control(0, 0, 0.3, 0, 2100)  # 向右
    rospy.loginfo("Right3!")

    paizhao()

    pos_control(0, 0, 0.3, 0, 2100)  # 向右
    rospy.loginfo("Right4!")

    paizhao()

    pos_control(0, 0, 0.3, 0, 2500)  # 向右
    rospy.loginfo("Right5!")

    paizhao()

    pos_control(0, 0, 0.3, 0, 2500)  # 向右
    rospy.loginfo("Right6!")

    paizhao()

    rospy.loginfo("Down!")
    pos_control(0, 0, 0, -0.3,1800)  # 向下

    paizhao()

    pos_control(0, 0, -0.3, 0, 2500)  # 向左
    rospy.loginfo("left1!")

    paizhao()

    pos_control(0, 0,-0.3, 0, 2500)  # 向左
    rospy.loginfo("left2!")

    paizhao()

    pos_control(0, 0, -0.3, 0, 2100)  # 向左
    rospy.loginfo("left3!")

    paizhao()

    pos_control(0, 0, -0.3, 0, 2100)  # 向左
    rospy.loginfo("left4!")

    paizhao()

    pos_control(0, 0, -0.3, 0, 2000)  # 向左
    rospy.loginfo("left5!")

    paizhao()

    pos_control(0, 0, -0.3, 0, 4000)  # 向左
    rospy.loginfo("left6!")

def second():
    pos_control(0, 0, 0.3, 0, 4000)  # 向右
    rospy.loginfo("Right1!")

    paizhao()

    pos_control(0, 0, 0.3, 0, 2000)  # 向右
    rospy.loginfo("Right2!")

    paizhao()
    
    pos_control(0, 0, 0.3, 0, 2100)  # 向右
    rospy.loginfo("Right3!")

    paizhao()

    pos_control(0, 0, 0.3, 0, 2100)  # 向右
    rospy.loginfo("Right4!")

    paizhao()

    pos_control(0, 0, 0.3, 0, 2500)  # 向右
    rospy.loginfo("Right5!")

    paizhao()

    pos_control(0, 0, 0.3, 0, 2500)  # 向右
    rospy.loginfo("Right6!")

    paizhao()

    rospy.loginfo("UP!")
    pos_control(0, 0, 0, 0.3,1800)  # 向上

    paizhao()

    pos_control(0, 0, -0.3, 0, 2500)  # 向左
    rospy.loginfo("left1!")

    paizhao()

    pos_control(0, 0,-0.3, 0, 2500)  # 向左
    rospy.loginfo("left2!")

    paizhao()

    pos_control(0, 0, -0.3, 0, 2100)  # 向左
    rospy.loginfo("left3!")

    paizhao()

    pos_control(0, 0, -0.3, 0, 2100)  # 向左
    rospy.loginfo("left4!")

    paizhao()

    pos_control(0, 0, -0.3, 0, 2000)  # 向左
    rospy.loginfo("left5!")

    paizhao()

    pos_control(0, 0, -0.3, 0, 5000)  # 向左
    rospy.loginfo("left6!")
    


if __name__ == '__main__':
    rospy.init_node('client')
    rospy.loginfo("Please set: 1-takeoff 2-landing 3-flightByOffset 4-flightByVel 5-gimbalControl")


    rospy.loginfo("Takeoff!")
    do_takeoff_or_landing(1) #起飞

    first()

    sleep(1)

    pos_control(0, 0.3, 0, 0, 7000)  # 向前
    rospy.loginfo("back!")

    sleep(1)

    second()

    sleep(1)

    pos_control(0, -0.3, 0, 0, 7000)  # 向后
    rospy.loginfo("back!!")

    sleep(1)

    # do_takeoff_or_landing(2)

    # # do_land()
    
    # sleep(1)
    
    # pos_control(0, 0, 0.1, 0, 10000)  # 向右
    # rospy.loginfo("Right 25000!")

    # sleep(1)

    # pos_control(0, 0, 0.1, 0, 10000)  # 向右
    # rospy.loginfo("Right 25000!")

    # sleep(1)

    # pos_control(0, 0, 0.1, 0, 5000)  # 向右
    # rospy.loginfo("Right 25000!")

    # sleep(1)


    # sleep(1)

    # pos_control(0, 0, -0.2, 0, 26000)  # 向左
    # rospy.loginfo("Right 25000!")

    # sleep(1)

    # do_takeoff_or_landing(2)

    rospy.loginfo("END!!!!")
