#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import os
import roslib.packages
from happymimi_voice_msgs.srv import StringToString,StringToStringResponse
#from std_srvs.srv import Empty
from happymimi_voice_msgs.srv import SpeechToText
from happymimi_msgs.srv import StrTrg
import re
import fuzzy
import copy
import yaml
import sys
happymimi_voice_path=roslib.packages.get_pkg_dir("happymimi_voice")+"/.."
sys.path.insert(0,happymimi_voice_path)
from happymimi_nlp import sentence_analysis as se
from happymimi_nlp import gender_judgement_from_name as GetGender


file_path=happymimi_voice_path+"/config/voice_common"
file_temp="/get_feature.txt"
name_path=roslib.packages.get_pkg_dir("find_my_mates")+"/config/guest_name.yaml"


class GetFeature():
    def __init__(self):
        rospy.init_node('get_feature_srv')
        with open(name_path) as f:
            self.names=yaml.safe_load(f)
        self.template=[s for s in open(file_path+file_temp)]
        self.GetGender=GetGender.GenderJudgementFromNameByNBC.loadNBCmodel(happymimi_voice_path+"/config/dataset/genderNBCmodel.dill")
        rospy.wait_for_service('/tts')
        rospy.wait_for_service('/stt_server')
        rospy.wait_for_service('/waveplay_srv')
        self.tts=rospy.ServiceProxy('/tts', StrTrg)
        self.wave_srv=rospy.ServiceProxy('/waveplay_srv', StrTrg)
        self.stt=rospy.ServiceProxy('/stt_server',SpeechToText)
        self.server=rospy.Service('/get_feature_srv',StringToString,self.main)
        #self.sound=rospy.ServiceProxy('/sound', Empty)

        self.name=""
        rospy.spin()


    def getName(self):
        self.wave_srv("WhatName")
        sentence=self.stt(short_str=False).result_str.lower()
        for name in self.names:
            str=sentence.replace(name.lower(),"{name}")

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
        self.wave_srv("WhatGender")
        sentence=self.stt(short_str=False).result_str
        str_ls=sentence.split()
        gender_ls=["woman","man","female","male"]
        for gender in gender_ls:
            for i in [i for i,x in enumerate(str_ls) if x==gender]:
                str_ls[i]="{gender}"
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
        if name=="female":
            name="woman"
        elif name=="male":
            name="man"

        return name


    def getOld(self):
        self.wave_srv("HowOld")
        sentence=self.stt(short_str=False).result_str
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
                result="man" if result=="male" else "woman"
            else:
                result=False

        if result:
            return StringToStringResponse(result_data=result,result=True)
        else:
            return StringToStringResponse(result=False)

if __name__=="__main__":

    GetFeature()
