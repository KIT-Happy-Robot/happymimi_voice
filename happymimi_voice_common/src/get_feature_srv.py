#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import os
import roslib.packages
from happymimi_voice_msgs.srv import StringToString,StringToStringResponse
#from std_srvs.srv import Empty
from happymimi_voice_msgs.srv import SpeechToText
from happymimi_msgs.srv import StrTrg,StrToStr,StrToStrResponse
import re
import fuzzy
import copy
import yaml
import sys
import math
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
        self.tempNumMake()
        with open(name_path) as f:
            self.names=yaml.safe_load(f)
        print(self.names)
        self.template=[s for s in open(file_path+file_temp)]
        self.GetGender=GetGender.GenderJudgementFromNameByNBC.loadNBCmodel(happymimi_voice_path+"/config/dataset/genderNBCmodel.dill")
        rospy.wait_for_service('/tts')
        rospy.wait_for_service('/stt_server')
        rospy.wait_for_service('/waveplay_srv')
        self.tts=rospy.ServiceProxy('/tts', StrTrg)
        self.wave_srv=rospy.ServiceProxy('/waveplay_srv', StrTrg)
        self.stt=rospy.ServiceProxy('/stt_server',SpeechToText)
        self.server=rospy.Service('/get_feature_srv',StrToStr,self.main)
        #self.sound=rospy.ServiceProxy('/sound', Empty)

        self.name=""
        rospy.spin()

    def tempNumMake(self):
        self.number=[]
        self.number_word=[]
        base1={'1':"one",'2':"two",'3':"three",'4':"four",'5':"five",'6':"six",'7':"seven",'8':"eight",'9':"nine",
        '10':"ten",'11':"eleven",'12':"twelve",'13':"thirteen",'14':"fourteen",'15':"fifteen",'16':"sixteen",'17':"seventeen",'18':"eighteen",'19':"nineteen",
        '2':"twenty",'3':"thirty",'4':"forty",'5':"fifty",'6':"sixty",'7':"seventy",'8':"eighty",'9':"ninety"}
        for k,v in base1.items():
            self.number.append(k)
            self.number_word.append(v)

    def getName(self):
        self.wave_srv("/WhatName2")
        #template=[i for i in self.template if "{name}" in i]
        sentence=self.stt(short_str=True,context_phrases=self.names,boost_value=20.0).result_str.lower()
        name=""
        current_name=""
        default_value=0.5

        for word in self.names:
            current_str,default_value=se.levSearch(word,sentence.split(),default_v=default_value,fuz=True,get_value=True)
            #print(word,default_value)
            if current_str!=-1:
                current_name=word
        if current_name!="":
            return current_name

        else:
            print("No such name")
            return False
        '''
        current_str=template[current_str].split()
        name = [i for i, x in enumerate(current_str) if x == "{name}"]
        result_str=copy.deepcopy(current_str)
        if name:
            self.name=se.wordVerification(sentence,current_str,result_str,name,self.names,"{name}")[0]
            print(self.name)
            return self.name
        else:
            print("no mach")
            return False
        '''


    def getGender(self):
        self.wave_srv("/WhatGender.wav")
        sentence=self.stt(short_str=False).result_str
        str_ls=sentence.split()
        template=[i for i in self.template if "{gender}" in i]
        gender_ls=["woman","man","female","male"]
        for gender in gender_ls:
            for i in [i for i,x in enumerate(str_ls) if x==gender]:
                str_ls[i]="{gender}"
        str=" ".join(str_ls)
        current_str=se.levSearch(str,template)
        if current_str==-1:
            return False
        current_str=template[current_str].split()
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
        self.wave_srv("/HowOld.wav")
        sentence=self.stt(short_str=True).result_str
        template=[i for i in self.template if "{num}" in i]
        num_ls=re.findall(r"\d+", sentence)
        str=""
        '''
        for num in num_ls:
            str=sentence.replace(num,"{num}")

        current_str=se.levSearch(str,template)

        if current_str==-1 or len(num_ls)==0:
            return False
        else:
            return num_ls[0]
        '''
        if(num_ls):
            return num_ls[0]
        else:
            sub_ls=[]
            current_str=-1
            for i in sentence.split():
                current_str=se.levSearch(i,self.number_word)
                if current_str!=-1:
                    sub_ls.append(self.number[current_str])
            if current_str==-1:
                return False
            else:
                return ''.join(sub_ls)

    def main(self,request):
        if request.req_data=="name":
            result=self.getName()
        elif request.req_data=="gender":
            result=self.getGender()
        elif request.req_data=="old":
            result=self.getOld()
        elif request.req_data=="predict gender":
            if self.name:
                print(self.name)
                result=self.GetGender.expectGender(self.name)
                result="man" if result=="male" else "woman"
            else:
                result=False

        if result:
            return StrToStrResponse(res_data=result,result=True)
        else:
            return StrToStrResponse(result=False)

if __name__=="__main__":

    GetFeature()
