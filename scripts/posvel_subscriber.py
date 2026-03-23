#!/usr/bin/env python3
import rospy
from posvel_control.msg import Posvel

def callback(data):
    rospy.loginfo("Received: x=%.2f, y=%.2f, dx=%.2f, dy=%.2f", 
                  data.x, data.y, data.dx, data.dy)

def listener():
    rospy.init_node('posvel_subscriber', anonymous=True)
    rospy.Subscriber('cmd_ctrl', Posvel, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
