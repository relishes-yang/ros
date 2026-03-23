#!/usr/bin/env python3
import rospy
from posvel_control.msg import Posvel

def talker():
    pub = rospy.Publisher('cmd_ctrl', Posvel, queue_size=10)
    rospy.init_node('posvel_publisher', anonymous=True)
    rate = rospy.Rate(10)  # 10 Hz
    
    while not rospy.is_shutdown():
        msg = Posvel()
        msg.x = 1.0
        msg.y = 2.0
        msg.dx = 0.1
        msg.dy = 0.2
        rospy.loginfo("Publishing: x=%.2f, y=%.2f, dx=%.2f, dy=%.2f", 
                      msg.x, msg.y, msg.dx, msg.dy)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
