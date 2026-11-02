#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
import math

class ScanFilter:
    def __init__(self):
        self.pub = rospy.Publisher('/scan_filtered', LaserScan, queue_size=1)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.callback, queue_size=1, buff_size=2**24)
        rospy.loginfo('Scan filter node initialized.')

    def callback(self, msg):
        new_ranges = list(msg.ranges)
        min_threshold = 0.28
        msg.range_min = max(msg.range_min, min_threshold)
        for i in range(len(new_ranges)):
            val = new_ranges[i]
            if math.isnan(val) or math.isinf(val) or val < min_threshold:
                new_ranges[i] = float('inf')
        msg.ranges = new_ranges
        self.pub.publish(msg)

if __name__ == '__main__':
    rospy.init_node('scan_filter_node')
    sf = ScanFilter()
    rospy.spin()
