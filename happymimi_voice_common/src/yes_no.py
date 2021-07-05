#!/usr/bin/env python
# -*- cording: utf-8 -*-

#発話
from gcp_texttospeech.srv import TTS
#音声認識
from voice_common_pkg.srv import SpeechToText

import rospy
from voice_common_pkg.srv import YesNo
from voice_common_pkg.srv import YesNoResponse

answer_list=['yes','no']

class GgiinStruction:
    def __init__(self):

        print("server is ready")
        rospy.wait_for_service('/tts')
        rospy.wait_for_service('/stt_server')
        self.server=rospy.Service('/yes_no',YesNo,self.yes_no)
        self.tts=rospy.ServiceProxy('/tts', TTS)
        self.stt=rospy.ServiceProxy('/stt_server',SpeechToText)
    def yes_no(self,req):
        while 1:
            str=self.stt(short_str=True,context_phrases=answer_list,
                    boost_value=15.0)
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
