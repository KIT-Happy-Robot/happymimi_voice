#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from happymimi_voice_msgs.srv import TTS

from happymimi_voice_msgs.srv import SpeechToText

import rospy
from happymimi_voice_msgs.srv import YesNo
from happymimi_voice_msgs.srv import YesNoResponse

answer_list=['yes','no']

class GgiinStruction:
    def __init__(self):

        print("server is ready")
        rospy.wait_for_service('/tts')
        rospy.wait_for_service('/stt_server2')
        self.server=rospy.Service('/yes_no',YesNo,self.yes_no)
        self.tts=rospy.ServiceProxy('/tts', TTS)
        self.stt=rospy.ServiceProxy('/stt_server2',SpeechToText)
    def yes_no(self,req):
        while 1:
            str=self.stt(short_str=True,context_phrases=answer_list,
                    boost_value=20.0)
            if answer_list[0] in str.result_str:
                return YesNoResponse(result=True)
            elif answer_list[1] in str.result_str:
                return YesNoResponse(result=False)
            else:
                pass


if __name__=='__main__':
    rospy.init_node("yes_no")
    GgiinStruction()
    rospy.spin()
