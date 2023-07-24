#!/usr/bin/env python3                                                      
# -*- coding: utf-8 -*-
#QRコードまたは音声認識で行動計画を生成するサービスサーバー
from PIL import Image
import requests
#QRコード読み込み
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from pyzbar.pyzbar import decode
import re

#音声認識
from happymimi_voice_msgs.srv import SpeechToText
#from happymimi_voice_msgs.srv import SpeechToTextResponse
from happymimi_voice_msgs.srv import ActPlan, ActPlanResponse
from happymimi_msgs.srv import StrTrg
import rospy
#モデルの読み込み
import predict_model

#文章の整形
import re

MODEL_PATH = "../resource/src3/" 

class ActPlanExecute():
    def __init__(self):
        
        rospy.loginfo("Wait for tts and stt")
        rospy.Subscriber('/camera/color/image_raw', Image, self.realsenseCB)
        rospy.wait_for_service('/tts')
        rospy.wait_for_service('/stt_server2')
        
        self.bridge = CvBridge()
        self.stt=rospy.ServiceProxy('/stt_server2',SpeechToText)
        self.server=rospy.Service('/planning_service',ActPlan,self.main)
        self.tts=rospy.ServiceProxy('/tts', StrTrg)
        
        rospy.loginfo("planning_service is ready")
    
    #画像の取得
    def realsenseCB(self, res):
        self.image_res = res
    
    #文章の整形が必要だね。まだ未完成
    def clean_sentence(sentence):

        pattern_r = "\w* room"
        pattern_n = "\w* name"
                
        if sentence in "room":
            result = re.findall(pattern_r,sentence,re.S)
            for i in range(len(result)):
                sentence = sentence.replace(str(result[i]), "\w*-room")
                
        elif sentence in "name":
            modified_sentence = sentence.replace("guest room", "guest-room")
        return sentence
    
    def main(self, request):
        
        data = request.way
        quesion_str = ""
        decoded_objects = []
        #QRコードでの処理
        if data == "qr":
            print("qr")
            while not decoded_objects:
                image = self.bridge.imgmsg_to_cv2(self.image_res)
                decoded_objects = decode(image)
                
            for obj in decoded_objects:
                quesion_str = str(obj.data)
                #print('Type : ', obj.type)
                #print('Data : ', obj.data)
        
            
        #音声認識  
        if data == "voice":
            self.tts("please task for me.")
            #文章認識
            quesion_str=self.stt(short_str=False)
            #整形した文章を取得
            #quesion = self.sentence_parse(str(quesion_str))
        
        try:
            rospy.loginfo(quesion_str)
        except UnboundLocalError:
            print("画像にQRが含まれていないか、音声が聞き取れません")
        
        #print(utt)
        #utt = self.clean_sentence(utt)
        #print(utt)
        
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

