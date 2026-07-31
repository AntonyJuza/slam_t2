#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped

def send_goal():
    rospy.init_node('test_goal_publisher', anonymous=True)
    pub = rospy.Publisher('/move_base_simple/goal_clean', PoseStamped, queue_size=1)
    rospy.sleep(1.0)
    
    goal = PoseStamped()
    goal.header.frame_id = "map"
    goal.header.stamp = rospy.Time.now()
    
    # Send a goal pose close to current robot pose (x: 0.3, y: 0.0)
    goal.pose.position.x = 0.3
    goal.pose.position.y = 0.0
    goal.pose.orientation.w = 1.0
    
    rospy.loginfo("Publishing test goal to /move_base_simple/goal_clean: x=0.3, y=0.0")
    pub.publish(goal)
    rospy.sleep(1.0)

if __name__ == '__main__':
    send_goal()
