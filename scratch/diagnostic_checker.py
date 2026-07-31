#!/usr/bin/env python
import rospy
import tf
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

class DiagnosticChecker:
    def __init__(self):
        rospy.init_node('diagnostic_checker', anonymous=True)

        self.last_odom = None
        self.last_cmd = None
        self.listener = tf.TransformListener()

        rospy.Subscriber('/cmd_vel', Twist, self.cmd_cb)
        rospy.Subscriber('/cmd_vel_nav', Twist, self.cmd_nav_cb)
        rospy.Subscriber('/odom_combined', Odometry, self.odom_cb)

        rospy.loginfo("=== Keenon T2 Diagnostic Monitor Started ===")
        rospy.loginfo("Monitoring: /cmd_vel, /cmd_vel_nav, /odom_combined, TF(odom->base_link)")

    def cmd_cb(self, msg):
        self.last_cmd = msg
        rospy.loginfo("[CMD_VEL (Chassis Input)] Linear.x: %+.3f, Angular.z: %+.3f", msg.linear.x, msg.angular.z)

    def cmd_nav_cb(self, msg):
        rospy.loginfo("[CMD_VEL_NAV (MoveBase Out)] Linear.x: %+.3f, Angular.z: %+.3f", msg.linear.x, msg.angular.z)

    def odom_cb(self, msg):
        px = msg.pose.pose.position.x
        py = msg.pose.pose.position.y
        vx = msg.twist.twist.linear.x
        wz = msg.twist.twist.angular.z

        rospy.loginfo("[ODOM] Pos(X: %+.3f, Y: %+.3f) | Vel(Vx: %+.3f, Wz: %+.3f)", px, py, vx, wz)

        # Check TF odom -> base_link
        try:
            (trans, rot) = self.listener.lookupTransform('odom', 'base_link', rospy.Time(0))
            roll, pitch, yaw = tf.transformations.euler_from_quaternion(rot)
            rospy.loginfo("[TF odom->base_link] Trans X: %+.3f, Y: %+.3f | Yaw: %+.3f rad (%+.1f deg)", 
                          trans[0], trans[1], yaw, math.degrees(yaw))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            pass

if __name__ == '__main__':
    checker = DiagnosticChecker()
    rospy.spin()
