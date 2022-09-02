#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from happymimi_msgs.srv import StrTrg
#from std_srvs.srv import Empty
from happymimi_voice_msgs.srv import SpeechToText

import Levenshtein as lev
import rospy
from happymimi_voice_msgs.srv import StringToString,StringToStringResponse
#filename and path
import os.path
import roslib.packages
import sys
happymimi_voice_path=roslib.packages.get_pkg_dir("happymimi_voice")+"/.."
sys.path.insert(0,happymimi_voice_path)
from happymimi_nlp import sentence_analysis as se
file_path=happymimi_voice_path+"/config/voice_common/"



class GgiinStruction:
    def __init__(self):

        rospy.wait_for_service('/stt_server')
        self.stt=rospy.ServiceProxy('/stt_server',SpeechToText)
        self.server=rospy.Service('/listen_command',StringToString,self.main)
        #self.sound=rospy.ServiceProxy('/sound', Empty)
        self.wave_srv=rospy.ServiceProxy('/waveplay_srv', StrTrg)


    def main(self,req):
        speak_list=[s.replace("\n","") for s in open(file_path+req.request_data)]
        #print(speak_list)
        self.wave_srv("/Ready.wav")
        string=self.stt(short_str=True,context_phrases=speak_list,boost_value=20.0).result_str

        current_str=se.levSearch(string,speak_list,fuz=True)
        if current_str!=-1:
            command=speak_list[current_str]
            success=True
        else:
            command=""
            success=False



        return StringToStringResponse(result_data=command,result=success)



if __name__=='__main__':
    rospy.init_node('listen_command')

    ggi=GgiinStruction()
    rospy.spin()
