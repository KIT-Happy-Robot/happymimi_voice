#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gcp_texttospeech.srv import TTS
 #音声認識
from voice_common_pkg.srv import SpeechToText
import rospy
from spr_speak.srv import SprInformation


class test():
    def __init__(self):
        rospy.loginfo('waiting service')
        rospy.wait_for_service('/spr_speak')
        rospy.wait_for_service('/tts')
        self.srv=rospy.ServiceProxy('/spr_speak',SprInformation)
        self.tts_srv=rospy.ServiceProxy('/tts', TTS)
    def main(self):
        response=self.srv("people 3")
        print(response.ans_str)
        self.tts_srv(response.ans_str)

if __name__=='__main__':
    rospy.init_node('test_spr')
    i=test()
    i.main()
