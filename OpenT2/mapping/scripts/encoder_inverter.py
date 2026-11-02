#!/usr/bin/env python
import rospy
from keenon_motor_msgs.msg import encoder

class EncoderInverter:
    def __init__(self):
        self.pub = rospy.Publisher('/encoder_raw_corrected', encoder, queue_size=10)
        self.sub = rospy.Subscriber('/encoder_raw', encoder, self.callback, queue_size=10)
        rospy.loginfo('Encoder inverter initialized: /encoder_raw -> /encoder_raw_corrected')

    def callback(self, msg):
        out = encoder()
        out.header = msg.header
        out.left = -msg.right
        out.right = -msg.left
        self.pub.publish(out)

if __name__ == '__main__':
    rospy.init_node('encoder_inverter')
    ei = EncoderInverter()
    rospy.spin()
