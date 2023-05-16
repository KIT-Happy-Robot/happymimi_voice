#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import whisper
import pyaudio
import wave
import sys, os
import rospy
import std_msgs
import smach
import yaml
import rosparam
import roslib.packages
from happymimi_voice_msgs.srv import *
from happymimi_msgs.srv import StrToStr, StrTrg, StrTrgResponse,SetFloat, SimpleTrg, SetStr, SetStrResponse

import pyaudio
import numpy as np
import Levenshtein as lev
import fuzzy
import nltk


file_name = "guest_name.yaml"
#file_path = roslib.packages.get_pkg_dir("happymimi_voice_common") + "/config/" + file_name
file_path = "/home/kouya/ros1_ws/src/happymimi_voice/config/voice_common/" + file_name

# [閾値]---------->
Threshold = 0.4
# <---------------------

# サンプリング周波数
fs = 44100
# 再生時間
duration = 0.3
# 生成する音の周波数
frequency = 880
# バッファサイズ
buffer_size = 1024
#音声認識の時間
record_second = 10
#生成する音声ファイル
#通常の再生では聞き取ることができない
wave_filename = "sample.wav"

# 音声出力関数（サービスクライアント）
tts_srv = rospy.ServiceProxy('/tts', StrTrg)
wave_srv = rospy.ServiceProxy('/waveplay_srv', StrTrg)

class Judgment_Name():
    
    def __init__(self):
        
        self.srv = rospy.ServiceProxy("/judgment_name", SetStr, self.main)
    
    #ピープ音を出す
    def start_sound(self,frequency, duration):
        
        # PyAudioのストリームを開く
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,channels=1,
                        rate=fs,output=True)
        
        t = np.linspace(0, duration, int(fs * duration), False)
        # 音を生成し、ストリームに書き込む
        samples = 0.1 * np.sin(frequency * 2 * np.pi * t)
        for i in range(0, len(samples), buffer_size):
            stream.write(samples[i:i+buffer_size].astype(np.float32).tobytes())
            
        # ストリームを閉じる
        stream.stop_stream()
        stream.close()
        p.terminate()
        

    def MakeWavFile(self,filename, Record_Seconds = 5):
        chunk = 1024
        FORMAT = pyaudio.paInt16

        CHANNELS = 1 #モノラル
        RATE = 44100 #サンプルレート（録音の音質）
        p = pyaudio.PyAudio()
        stream = p.open(format = FORMAT,
                        channels = CHANNELS,
                        rate = RATE,
                        input = True,
                        frames_per_buffer = chunk)
        #レコード開始
        print("Now Recording...")
        all = []
        for i in range(0, int(RATE / chunk * Record_Seconds)):
            data = stream.read(chunk) #音声を読み取って、
            all.append(data) #データを追加
        #レコード終了
        print("Finished Recording.")
        stream.close()
        p.terminate()
        wavFile = wave.open(wave_filename, 'wb')
        wavFile.setnchannels(CHANNELS)
        wavFile.setsampwidth(p.get_sample_size(FORMAT))
        wavFile.setframerate(RATE)
        #wavFile.writeframes(b''.join(all)) #Python2 用
        wavFile.writeframes(b"".join(all)) #Python3用
        wavFile.close()

    def clean_sentence(self,sentence):
        morph = nltk.word_tokenize(sentence)
        guest_name = ""
        pos = nltk.pos_tag(morph)
        for i,w in enumerate(pos):
            print(w)
            if w[1] == "NNP" or w[1] == "NN":    
                guest_name = w[0]
            
        #print(guest_name)
        return guest_name

    def read_guest_name(self):
        guest_name_list_m = []
        guest_name_list_f = []
        num = 1
        with open(file_path) as yl:
            config = yaml.safe_load(yl)
            for i,w in enumerate(config["Female"]):
                #print(w)
                guest_name_list_f.append(config["Female"][w])
                num += 1
            
            num = 1   
            for i,w in enumerate(config["Male"]):
                #print(w)
                guest_name_list_m.append(config["Male"][w])
                num += 1
                
        #print(guest_name_list_f)
        #print(guest_name_list_m)
        return guest_name_list_f, guest_name_list_m

    def lev_distance(self,sentence, base):
        phonetic_base = fuzzy.nysiis(base)
        phonetic_target = fuzzy.nysiis(sentence)
        
        return lev.distance(phonetic_base, phonetic_target)\
                    /(max(len(phonetic_base), len(phonetic_target))* 1.00)

    def getDistanceList(self,sentence,guest_name):
            distance_list = []
            for w in guest_name:
                distance_list.append(self.lev_distance(w, sentence))
            
            closest_distance = min(distance_list)
            #print(distance_list)
            if closest_distance >= Threshold:
                return [None, None]
            else:
                num = distance_list.index(closest_distance)
                
            return guest_name[num]

    def main(self):
        self.start_sound(frequency=frequency, duration=duration)
        self.MakeWavFile(wave_filename, Record_Seconds = 5)    
        model = whisper.load_model("small",in_memory=True)
        result = model.transcribe(wave_filename, verbose=False, language="en")
        
        #print(result["text"])
        #学内環境だとプロキシに引っかかる
        
        name = self.clean_sentence(result["text"])
        tts_srv(result["text"])
        guest_name_list_f, guest_name_list_m = self.read_guest_name()
        
        #print(name)
        #男女どちらも可能
        print(self.getDistanceList(name,guest_name_list_f))
        print(self.getDistanceList(name,guest_name_list_m))
        
        #今回は試験的に男性側で特定
        return SetStrResponse(result = self.getDistanceList(name,guest_name_list_m))
    
    
if __name__ == "__main__":
    rospy.init_node('judment_name')
    JN = Judgment_Name()
    rospy.spin()
    