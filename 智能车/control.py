import rospy
from geometry_msgs.msg import Twist
import time
def move_forward(distance,fx,linear_speed):
    rospy.init_node('move_forward_node')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 设置发布频率为10hz

    # 设置线速度为0.2 m/s
    
    num=fx
    # 计算运行时间（根据速度和距离的关系）
    duration = abs(distance / linear_speed)
    print(num)
    # 创建移动指令
    cmd_vel_msg = Twist()
    if num == 0:
    	cmd_vel_msg.linear.x = linear_speed
    if num == 1:
        cmd_vel_msg.linear.y = linear_speed
    cmd_vel_msg.angular.z = 0.0
    start_time = rospy.Time.now()  # 记录开始时间

    while (rospy.Time.now() - start_time).to_sec() < duration:
        print((rospy.Time.now() - start_time).to_sec())
        pub.publish(cmd_vel_msg)
        rate.sleep()

    # 发布停止指令以停止机器人运动
    print("已行使（米）：")
    print(distance)
    cmd_vel_msg.linear.y = 0.0
    cmd_vel_msg.linear.y = 0.0
    pub.publish(cmd_vel_msg)

if __name__ == '__main__':
    try:
        while 1:
            
            #print("已行使（米）：")
            move_forward(6.5,1,-0.2) 
            time.sleep(3)
            move_forward(1.7,0,0.2) 
            time.sleep(3)
            move_forward(6.5,1,0.2) 
            time.sleep(3)
            move_forward(1.7,0,-0.2)
            
    except rospy.ROSInterruptException:
        pass
