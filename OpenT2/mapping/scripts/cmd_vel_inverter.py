#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

class CmdVelInverter:
    def __init__(self):
        self.invert_linear = rospy.get_param('~invert_linear', True)
        self.invert_angular = rospy.get_param('~invert_angular', False)
        self.output_topic = rospy.get_param('~output_topic', '/cmd_vel_chassis')
        
        self.pub = rospy.Publisher(self.output_topic, Twist, queue_size=1)
        self.sub_vel = rospy.Subscriber('/cmd_vel', Twist, self.callback, queue_size=1)
        self.sub_nav = rospy.Subscriber('/cmd_vel_nav', Twist, self.callback, queue_size=1)
        self.sub_teleop = rospy.Subscriber('/cmd_vel_teleop', Twist, self.callback, queue_size=1)
        rospy.loginfo('cmd_vel_inverter initialized. invert_linear=%s, invert_angular=%s, output=%s', 
                      self.invert_linear, self.invert_angular, self.output_topic)

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
