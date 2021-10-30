#! /usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################
#ed 2021/9/17
#author fukuda nao
#############################################################

from happymimi_voice_msgs.srv import TTS
#音声認識
from happymimi_voice_msgs.srv import SpeechToText
from happymimi_voice_msgs.srv import ActionPlan
from happymimi_voice_msgs.srv import ActionPlanResponse
import pickle
import rospy
import sentence_parsing
import rospy
#origin
import sentence_parsing





class ActionPlanning():
    def __init__(self):

        rospy.loginfo("Waiting for stt and tts")
        rospy.wait_for_service('/tts')
        rospy.wait_for_service('/stt_server')
        self.stt=rospy.ServiceProxy('/stt_server',SpeechToText)
        self.server=rospy.Service('/planning_srv',ActionPlan,self.main)
        self.tts=rospy.ServiceProxy('/tts', TTS)
        self.str_pars=sentence_parsing.SentenceParsing()
        rospy.loginfo("planning_srv is ready")

    def main(self,request_msg):
        self.tts("please question for me")

        quesion_str=self.stt(short_str=False)
        current_quetion=self.str_pars.questionFormating(quesion_str.result_str)
        if current_quetion=="ERROR":
            self.tts("pardon?")
            return ActionPlanResponse(result=False)
        elif not self.str_pars.availabilityJudgement(current_quetion):
            self.tts("I can't answer")
            return ActionPlanResponse(result=False)

        self.tts(current_quetion)

        action_ls,target_ls=self.str_pars.makePlan(current_quetion)
        #print(action_ls,target_ls)
        for k,v in zip(action_ls,target_ls):
            self.tts(k+" "+v)
        if(action_ls==None):
            self.tts("pardon?")
            return ActionPlanResponse(result=False)
        else:
            print(action_ls,target_ls)
            return ActionPlanResponse(result=True, action=action_ls, data=target_ls)

if __name__=="__main__":
    rospy.init_node('planning_srv')
    a=ActionPlanning()
    rospy.spin()
