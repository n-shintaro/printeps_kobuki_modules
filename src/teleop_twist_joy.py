#!/usr/bin/env python
#import roslib; roslib.load_manifest('teleop_twist_joy')
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


class JoyTwist(object):
    def __init__(self):
        self._joy_sub   = rospy.Subscriber('joy', Joy, self.joy_callback, queue_size=1)
        self._twist_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=2)
        self.max_speed  = rospy.get_param('~max_speed', 0.8)
        self.max_turn   = rospy.get_param('~max_turn', 2.0)
        self.release=True
    def joy_callback(self, joy_msg):

        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        buttom=False
        #print "joy_msg:", joy_msg
        print "joy_msg.buttons:", joy_msg.buttons
        print "joy_msg.buttons[5]:", joy_msg.buttons[5]
        # Translational motion --------------------------

        if joy_msg.buttons[0] == 1:
            twist.linear.x = joy_msg.axes[1] * self.max_speed
            twist.linear.y = joy_msg.axes[0] * self.max_speed
            buttom=True

        # Rotational motion -----------------------------
        if joy_msg.buttons[4] == 1 and joy_msg.buttons[5] == 0:
            twist.angular.z = self.max_turn
            buttom=True

        if joy_msg.buttons[4] == 0 and joy_msg.buttons[5] == 1:
            twist.angular.z = -self.max_turn
            buttom=True

        
        if buttom:
            print twist
            self._twist_pub.publish(twist)
            self.release=True

        elif self.release:
            self._twist_pub.publish(twist)
            print twist
            self.release=False
        


if __name__=="__main__":

    rospy.init_node('teleop_twist_joy')
    joy_twist = JoyTwist()
    rospy.spin()
