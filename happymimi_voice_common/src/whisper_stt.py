#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import whisper
import pyaudio
import wave
import rospy 
from happymimi_msgs.srv import SetStr, SetStrResponse

class Whisper_Stt:
    
    def __init__(self):
        
        self.FORMAT = pyaudio.paInt16
        self.wave_filename = "sample.wav"
        self.CHUNK = 1024
        self.RECORD_SECOND = 5
        self.CHANNELS = 1 #モノラル
        self.RATE = 44100 #サンプルレート（録音の音質）
        
        print("whisper_ready")
        self.srv = rospy.Service("/whisper_stt",SetStr,self.whisper_server)
        
    def MakeWavFile(self):
        
        p = pyaudio.PyAudio()
        stream = p.open(format = self.FORMAT,
                        channels = self.CHANNELS,
                        rate = self.RATE,
                        input = True,
                        frames_per_buffer = self.CHUNK)
        #レコード開始
        print("Now Recording...")
        all = []
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECOND)):
            data = stream.read(self.CHUNK) #音声を読み取って、
            all.append(data) #データを追加
        #レコード終了
        
        print("Finished Recording.")
        stream.close()
        p.terminate()
        wavFile = wave.open(self.wave_filename, 'wb')
        wavFile.setnchannels(self.CHANNELS)
        wavFile.setsampwidth(p.get_sample_size(self.FORMAT))
        wavFile.setframerate(self.RATE)
        #wavFile.writeframes(b''.join(all)) #Python2 用
        wavFile.writeframes(b"".join(all)) #Python3用
        wavFile.close()

    def whisper_server(self,_):
        
        self.MakeWavFile()
        #この読み込みを高速化したいかも
        #実機でのデバッグはdevice="GPU"に変更して 
        #model = whisper.load_model(name="large",device="cpu",in_memory=True) #子機デバッグ用
        model = whisper.load_model(name="large",device="cpu",in_memory=True) #実機デバッグ用
        _ = model.half()
        _ = model.cuda()
        
        result = model.transcribe(self.wave_filename, verbose=False, language="en")
        print(result["text"]) 
        
        return SetStrResponse(result = result["text"])   
        

if __name__ == "__main__":    
    rospy.init_node("whisper_stt")
    ws = Whisper_Stt()
    rospy.spin()
    
    #model = whisper.load_model(name="large",device="cpu",in_memory=True)
    #result = model.transcribe(whisper_stt.wave_filename, verbose=False, language="en")
    #print(result["text"])