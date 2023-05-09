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
from happymimi_msgs.srv import StrToStr, StrTrg, SetFloat, SimpleTrg, SetStr

import pyaudio
import numpy as np

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

#ピープ音を出す
def start_sound(frequency, duration):
    
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
    

def MakeWavFile(filename, Record_Seconds = 5):
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




def main():
    start_sound(frequency=frequency, duration=duration)
    MakeWavFile(wave_filename, Record_Seconds = 5)    
    model = whisper.load_model("small",in_memory=True)
    result = model.transcribe(wave_filename, verbose=False, language="en")
    
    print(result["text"])
    #学内環境だとプロキシに引っかかる
    tts_srv(result["text"])
    
if __name__ == "__main__":
    main()