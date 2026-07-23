#!/usr/bin/env python
import rospy
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import PointCloud2, LaserScan
from nav_msgs.msg import OccupancyGrid

class TFCleaner:
    def __init__(self):
        self.tf_pub = rospy.Publisher('/tf_clean', TFMessage, queue_size=100)
        self.tf_static_pub = rospy.Publisher('/tf_static_clean', TFMessage, queue_size=100)
        self.bump_pub = rospy.Publisher('/bump_clean', PointCloud2, queue_size=10)
        self.scan_pub = rospy.Publisher('/scan_filtered_clean', LaserScan, queue_size=10)
        self.map_pub = rospy.Publisher('/map_clean', OccupancyGrid, queue_size=1, latch=True)

        self.tf_sub = rospy.Subscriber('/tf', TFMessage, self.tf_callback)
        self.tf_static_sub = rospy.Subscriber('/tf_static', TFMessage, self.tf_static_callback)
        self.bump_sub = rospy.Subscriber('/bump', PointCloud2, self.bump_callback)
        self.scan_sub = rospy.Subscriber('/scan_filtered', LaserScan, self.scan_callback)
        self.map_sub = rospy.Subscriber('/map', OccupancyGrid, self.map_callback)
        rospy.loginfo("TF Cleaner node initialized.")

    def clean_tf_msg(self, msg):
        cleaned_transforms = []
        for t in msg.transforms:
            fid = t.header.frame_id
            cid = t.child_frame_id
            if not fid or not cid:
                continue
            # Strip leading slash
            if fid.startswith('/'):
                t.header.frame_id = fid.lstrip('/')
            if cid.startswith('/'):
                t.child_frame_id = cid.lstrip('/')
            cleaned_transforms.append(t)
        msg.transforms = cleaned_transforms
        return msg

    def tf_callback(self, msg):
        cleaned = self.clean_tf_msg(msg)
        if cleaned.transforms:
            self.tf_pub.publish(cleaned)

    def tf_static_callback(self, msg):
        cleaned = self.clean_tf_msg(msg)
        if cleaned.transforms:
            self.tf_static_pub.publish(cleaned)

    def bump_callback(self, msg):
        if msg.header.frame_id.startswith('/'):
            msg.header.frame_id = msg.header.frame_id.lstrip('/')
        self.bump_pub.publish(msg)

    def scan_callback(self, msg):
        if msg.header.frame_id.startswith('/'):
            msg.header.frame_id = msg.header.frame_id.lstrip('/')
        self.scan_pub.publish(msg)

    def map_callback(self, msg):
        if msg.header.frame_id.startswith('/'):
            msg.header.frame_id = msg.header.frame_id.lstrip('/')
        self.map_pub.publish(msg)

if __name__ == '__main__':
    rospy.init_node('tf_cleaner_node')
    cleaner = TFCleaner()
    rospy.spin()

