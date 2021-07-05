#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gcp_texttospeech.srv import TTS
#from std_srvs.srv import Empty
from voice_common_pkg.srv import SpeechToText

import Levenshtein as lev
import rospy
from voice_common_pkg.srv import ListenCommand
from voice_common_pkg.srv import ListenCommandResponse
#filename and path
import os.path

file_path=os.path.expanduser('~/catkin_ws/src/voice_common_pkg/config')



class GgiinStruction:
    def __init__(self):

        print("server is ready")
        rospy.wait_for_service('/tts')
        rospy.wait_for_service('/stt_server')
        self.stt=rospy.ServiceProxy('/stt_server',SpeechToText)
        self.server=rospy.Service('/listen_command',ListenCommand,self.main)
        #self.sound=rospy.ServiceProxy('/sound', Empty)
        self.tts=rospy.ServiceProxy('/tts', TTS)


    def main(self,req):
        with open(file_path+req.file_name,'r') as f:
            speak_list=[line.strip() for line in f.readlines()]
        self.tts("ready")
        string=self.stt(short_str=True,context_phrases=speak_list,boost_value=20.0)
        num_lev=1
        prog_num=-1
        for str_num in range(len(speak_list)):
            result = lev.distance(string.result_str, speak_list[str_num])/(max(len(string.result_str), len(speak_list[str_num])) *1.00)

            if result <0.2:
                prog_num=str_num
                break

            elif num_lev>result and result<0.5:
                num_lev=result
                prog_num=str_num

        success=False
        if prog_num<0 or prog_num>=len(speak_list):
            command=''
            success=False
        else:
            command=speak_list[prog_num]
            success=True


        return ListenCommandResponse(cmd=command,result=success)



if __name__=='__main__':
    rospy.init_node('listen_command')

    ggi=GgiinStruction()
    rospy.spin()
