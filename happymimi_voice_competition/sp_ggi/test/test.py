#!/usr/bin/env python
# -*- cording: utf-8 -*-


import rospy
import actionlib
from ggi.srv import ListenCommand

def call_service():
    rospy.loginfo('waiting service')

    rospy.wait_for_service('/listen_command')
    try:
        service = rospy.ServiceProxy('/listen_command', ListenCommand)
        while 1:
            response = service()
            if response.result:
                print(response.cmd)
                break
            else:
                continue
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e

if __name__ == "__main__":
    rospy.init_node('listen_test')
    call_service()
