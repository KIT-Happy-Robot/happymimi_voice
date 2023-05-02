#!/usr/bin/env python3                                                      
# -*- coding: utf-8 -*-
#QRコードまたは音声認識で行動計画を生成するサービスサーバー

#QRコード読み込み
import cv2
#from happymimi_voice_msgs.srv import TTS
import re
#音声認識
from happymimi_voice_msgs.srv import SpeechToText
#from happymimi_voice_msgs.srv import SpeechToTextResponse
from happymimi_voice_msgs.srv import ActPlan, ActPlanResponse
from happymimi_msgs.srv import StrTrg
import rospy
#モデルの読み込み
import predict_model

MODEL_PATH = "../resource/src3/" 

class ActPlanExecute():
    def __init__(self):
        
        rospy.loginfo("Wait for tts and stt")
        rospy.wait_for_service('/tts')
        rospy.wait_for_service('/stt_server2')
        self.stt=rospy.ServiceProxy('/stt_server2',SpeechToText)
        self.server=rospy.Service('/planning_service',ActPlan,self.main)
        self.tts=rospy.ServiceProxy('/tts', StrTrg)
        
        rospy.loginfo("planning_service is ready")
    
    #文章の整形
    def sentence_parse(self, sen):
        for str in sen:
                    sentence = str.lower().strip()
                    sentence = re.sub(r"([?.!,¿])", r" \1 ", sentence)
                    sentence = re.sub(r'[" "]+', " ", sentence)
                    sentence = re.sub(r"[^a-zA-Z?.!,¿]+", " ", sentence)
                    sentence = sentence.rstrip(" .").strip()
        
        print(sentence)
        return sentence
     
    def main(self, _):
        self.tts("please task for me.")
        #文章認識
        quesion_str=self.stt(short_str=False)
        #整形した文章を取得
        #quesion = self.sentence_parse(str(quesion_str))
        
        rospy.loginfo(quesion_str)
        for utt in [str(quesion_str)]:
            concept = predict_model.extract_crf(utt)
            da = predict_model.extract_svc(utt)
            keys_list = list(concept.keys())
            values_list = list(concept.values())
            
             
        return ActPlanResponse(concept=keys_list, data=values_list, da=da)
    
if __name__ == "__main__":
    rospy.init_node('planning_service')
    actplan_exe = ActPlanExecute()
    #actplan_exe.main()
    rospy.spin()