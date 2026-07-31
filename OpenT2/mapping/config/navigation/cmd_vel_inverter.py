#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

class CmdVelInverter:
    def __init__(self):
        self.invert_linear = rospy.get_param('~invert_linear', True)
        self.invert_angular = rospy.get_param('~invert_angular', False)
        
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.sub_nav = rospy.Subscriber('/cmd_vel_nav', Twist, self.callback, queue_size=1)
        self.sub_teleop = rospy.Subscriber('/cmd_vel_teleop', Twist, self.callback, queue_size=1)
        rospy.loginfo("cmd_vel_inverter initialized. Listening on /cmd_vel_nav and /cmd_vel_teleop -> Publishing to /cmd_vel")

    def callback(self, msg):
        out_msg = Twist()
        out_msg.linear.x = -msg.linear.x if self.invert_linear else msg.linear.x
        out_msg.linear.y = msg.linear.y
        out_msg.linear.z = msg.linear.z
        
        out_msg.angular.x = msg.angular.x
        out_msg.angular.y = msg.angular.y
        out_msg.angular.z = -msg.angular.z if self.invert_angular else msg.angular.z
        
        self.pub.publish(out_msg)

if __name__ == '__main__':
    rospy.init_node('cmd_vel_inverter')
    inverter = CmdVelInverter()
    rospy.spin()
