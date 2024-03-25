#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#pip install -U openai-whisper
import whisper
import pyaudio
import wave
import rospy 
import roslib.packages
happymimi_voice_path=roslib.packages.get_pkg_dir("happymimi_voice")+"/../config/wave_data/PI.wav"

from happymimi_msgs.srv import SetStr, SetStrResponse

class Whisper_Stt:
    
    def __init__(self):
        
        self.FORMAT = pyaudio.paInt16
        self.wave_filename = "sample.wav"
        self.CHUNK = 1024
        self.RECORD_SECOND = 24
        self.CHANNELS = 1 #モノラル
        self.RATE = 44100 #サンプルレート（録音の音質）
        self.closed = True
        
        #model = whisper.load_model(name="large",device="cpu",in_memory=True) #実機デバッグ用
        #_ = model.half()
        #_ = model.cuda()
        self.model = whisper.load_model(name="large",device="cpu",in_memory=True) #子機デバッグ用
        _ = self.model.half()
        _ = self.model.cuda()
        
        for m in self.model.modules():
            if isinstance(m, whisper.model.LayerNorm):
                m.float()

        
        print("whisper_ready")
        self.srv = rospy.Service("/whisper_stt",SetStr,self.whisper_server)
    
    def sound_pi(self):
        try:
            wf = wave.open(happymimi_voice_path, "rb")
            print("Time[s]:", float(wf.getnframes()) / wf.getframerate())
        except FileNotFoundError:
            pass
        p = pyaudio.PyAudio()
        stre = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        chunk = 1024
        data = wf.readframes(chunk)
        while data != b'':
            stre.write(data)
            data = wf.readframes(chunk)
        stre.stop_stream()
        stre.close()
        p.terminate()
        wf.close()
        self.closed = False

        return self

    
    def MakeWavFile(self):
        
        p = pyaudio.PyAudio()
        stream = p.open(format = self.FORMAT,
                        channels = self.CHANNELS,
                        rate = self.RATE,
                        input = True,
                        frames_per_buffer = self.CHUNK)
        #レコード開始
        self.sound_pi()
        print("Now Recording...")
        all = []
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECOND)):
            data = stream.read(self.CHUNK) #音声を読み取って、
            all.append(data) #データを追加
        #レコード終了
        self.sound_pi()
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
        result = self.model.transcribe(
            self.wave_filename, 
            verbose=False, 
            language="en",
            beam_size=5,
            fp16=True,
            without_timestamps=True
        )
        print(result["text"]) 
        
        return SetStrResponse(result = result["text"])   
        
    def Sentence_correction(self, text):    
        print("--start correction--")
        

if __name__ == "__main__":    
    rospy.init_node("whisper_stt")
    ws = Whisper_Stt()
    rospy.spin()
    
    #model = whisper.load_model(name="large",device="cpu",in_memory=True)
    #result = model.transcribe(whisper_stt.wave_filename, verbose=False, language="en")
    #print(result["text"])
