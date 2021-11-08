#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import os
import roslib.packages
from happymimi_voice_msgs.srv import StringToString,StringToStringResponse
#from std_srvs.srv import Empty
from happymimi_voice_msgs.srv import SpeechToText
import re
import fuzzy
import copy
from ../happymimi_nlp import sentence_analysis as se
from ../happymimi_nlp import gender_judgement_from_name　as GetGender

file_path=roslib.packages.get_pkg_dir("happymimi_voice")+"/config/voice_common"
file_name="/names.txt"
file_temp="/get_feature.txt"
class GetFeature():
    def __init__(self):

        self.names=[name for name in open(file_path+file_name)]
        self.template=[s for s in open(file_path+file_temp)]
        self.GetGender=GetGender.GenderJudgementFromNameByNBC.loadNBCmodel()
        rospy.wait_for_service('/tts')
        rospy.wait_for_service('/stt_server')
        self.stt=rospy.ServiceProxy('/stt_server',SpeechToText)
        self.server=rospy.Service('/get_feature_srv',StringToString,self.main)
        #self.sound=rospy.ServiceProxy('/sound', Empty)
        self.tts=rospy.ServiceProxy('/tts', TTS)
        self.name=""
        rospy.spin()


    def getName(self):
        self.tts("what's your name?")
        sentence=self.stt(short_str=False)
        for name in self.names:
            str=sentence.replace(name,"{name}")

        current_str=self.template[se.levSearch(str,self.template)].split()
        if current_str==-1:
            return False
        name = [i for i, x in enumerate(current_str) if x == "{name}"]
        result_str=copy.deepcopy(current_str)
        if name:
            self.name=se.wordVerification(sentence,current_str,result_str,name,self.names,"{name}")[0]
            return self.name
        else:
            return False


    def getGender(self):
        self.tts("What's your gender")
        sentence=self.stt(short_str=False)
        str_ls=sentence.split()
        gender_ls=["woman","man","female","male"]
        for gender in gender_ls:
            index_ge=[i for i,x in enumerate(str_ls) if x==gender]
            [str_ls[i]="{gender}" for i in index_ge]
        str=" ".join(str_ls)
        current_str=self.template[se.levSearch(str,self.template)].split()
        if current_str==-1:
            return False

        name = [i for i, x in enumerate(current_str) if x == "{gender}"]
        result_str=copy.deepcopy(current_str)
        if name:
            name=se.wordVerification(sentence,current_str,result_str,name,gender_ls,"{gender}")[0]
        else:
            return False


    def getOld(self):
        self.tts("How old are you?")
        sentence=self.stt(short_str=False)
        num_ls=re.findall(r"\d+", sentence)
        for num in num_ls:
            str=sentence.replace(num,"{num}")

        current_str=self.template[se.levSearch(str,self.template)]
        if current_str==-1 or len(num_ls)==0:
            return False
        else:
            return num_ls[0]


    def main(self,request):
        if request.request_data=="name":
            result=self.getName()
        elif request.request_data=="gender":
            result=self.getGender()
        elif request.request_data=="old":
            result=self.getOld()
        elif request.request_data=="predict gender":
            if self.name:
                result=self.GetGender.expectGender(self.name)
            else:
                result=False

        if result:
            return StringToStringResponse(result_data=result,result=True)
        else:
            return StringToStringResponse(result=False)
