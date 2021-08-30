#! /usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(message):

    print(message.data)

def listener():

    rospy.init_node('listener', anonymous=True)

    sub = rospy.Subscriber('/setup_location/location_name', String, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()
