import rospy
import math
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry

def get_yaw(q):
    return math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z)) * 180.0 / math.pi

last_imu_yaw = 0.0
last_odom_yaw = 0.0

def imu_callback(msg):
    global last_imu_yaw
    last_imu_yaw = get_yaw(msg.orientation)

def odom_callback(msg):
    global last_odom_yaw
    last_odom_yaw = get_yaw(msg.pose.pose.orientation)

rospy.init_node('test_yaw_node')
rospy.Subscriber('/chassis_imu_data', Imu, imu_callback)
rospy.Subscriber('/odom_combined', Odometry, odom_callback)

r = rospy.Rate(5)
print("Starting yaw monitor. Please rotate the robot...")
while not rospy.is_shutdown():
    print("IMU Yaw: %.2f deg | Odom Yaw: %.2f deg" % (last_imu_yaw, last_odom_yaw))
    r.sleep()
