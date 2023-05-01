#!/usr/bin/env python3                                                      
# -*- coding: utf-8 -*-
#QRコードまたは音声認識で行動計画を生成するサービスサーバー

#QRコード読み込み
import cv2
from happymimi_voice_msgs.srv import TTS
#音声認識
from happymimi_voice_msgs.srv import SpeechToText
import rospy
#モデルの読み込み
import predict_model

class ActPlanExecute():
    def __init__(self) -> None:
        
        rospy.loginfo("Wait for tts and stt")
        rospy.wait_for_service('/tts')
        rospy.wait_for_service('/stt_server')
        self.stt=rospy.ServiceProxy('/stt_server',SpeechToText)
        self.tts=rospy.ServiceProxy('/tts', TTS)
        rospy.loginfo("planning_service is ready")