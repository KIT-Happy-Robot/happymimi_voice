#!/usr/bin/env python
# -*- coding: utf-8 -*-

from voice_common_pkg.srv import TTS
#音声認識
from voice_common_pkg.srv import SpeechToText

import rospy
import Levenshtein as lev

from voice_common_pkg.srv import SprInformation
from voice_common_pkg.srv import SprInformationResponse
import os.path
import sys
sys.path.insert(0,os.path.expanduser('~')+"/catkin_ws/src/mimi_micarray_pkg/src")
from respeaker_function import *
file_path=os.path.expanduser('~/catkin_ws/src/voice_common_pkg/config') #作成場所の指定

class RecognitionAnswer():
    def __init__(self):
        self.question_list=[]
        self.answer_list=[]

        with open(file_path+"/question_answer",'r') as f:
            for str in f:
                if "q:" in str:
                    self.question_list.append(str.replace('q:', ''))
                else:
                    self.answer_list.append(str.replace('a:', ''))

        self.respeaker_sub=respeaker()
        rospy.wait_for_service('/tts')
        rospy.wait_for_service('/stt_server')
        self.stt_srv=rospy.ServiceProxy('/stt_server',SpeechToText)
        #rospy.Service('/spr_QA',SprInformation,self.main)
        self.tts_srv=rospy.ServiceProxy('/tts', TTS)
        print('server is ready')
        rospy.Service('/spr_speak',SprInformation,self.main)
        rospy.spin()
        self.respeaker_sub=respeaker()
        self.angle=0

    def select_question(self):
        decision_number = 0.6
        decision_sub = 0.0
        question = -1

        while(question==-1):
            string=self.stt_srv(short_str=False)
            self.angle = self.respeaker_sub.sound_direction()
            print(self.angle,type(self.angle))
            for i in range(len(self.question_list)):
                decision_sub=lev.distance(string.result_str, self.question_list[i])/(max(len(string.result_str), len(self.question_list[i])) *1.00)
                if decision_sub<decision_number:
                    decision_number=decision_sub
                    question=i
            if question==-1:
                self.tts_srv('please one more time')



        return question

    def answer_make(self,str,question):
        lavel_ls=[]
        value_ls=[]
        #ラベルと値を分けて添字で紐付けできるように
        for cnt,info in enumerate(str.split()):
            if cnt%2==0:
                lavel_ls.append('{'+info+'}')
            else:
                value_ls.append(info)

        #ラベル検索・値の置き換え
        for cnt,lavel in enumerate(lavel_ls):
            if lavel in self.answer_list[question]:
                str=self.answer_list[question].replace(lavel,value_ls[cnt])
                self.answer_list[question]=str



    def main(self,req):
        answer_num = self.select_question()
        self.answer_make(req.some_info,answer_num)

        return SprInformationResponse(ans_str=self.answer_list[answer_num],respeaker_angle=self.angle)





if __name__=='__main__':
    rospy.init_node('spr_QA')
    i=RecognitionAnswer()
    i.main()
