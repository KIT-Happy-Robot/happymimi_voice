#!/usr/bin/env python
# -*- cording: utf-8 -*-


import rospy
from ggi.srv import GgiLearning

def call_service():
    rospy.loginfo('waiting service')

    rospy.wait_for_service('/ggi_learning')
    try:
        service = rospy.ServiceProxy('/ggi_learning',GgiLearning)
        response = service()
        print(response.result)
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e

if __name__ == "__main__":
    rospy.init_node('training_test')
    call_service()
