#! /usr/bin/env python3
#-*- coding: utf-8 -*-
#[tts_stdserver.py]

import roslib
import rospy
#from happymimi_voice_msgs.srv import TTS, TTSResponse
from happymimi_msgs.srv import StrTrg,StrTrgResponse
from google.cloud import texttospeech

import wave
import pyaudio

import os
from subprocess import PIPE
import subprocess

Filename = 'output.wav'
#bashrcに書き込んでおくべし！
password = (os.environ["SUDO_KEY"] + "\n").encode()

#プロキシ対策
def check_wifi():
    proc = subprocess.run(["sudo","-S","wpa_cli", "status"],stdout = subprocess.PIPE, stderr = subprocess.PIPE, input=password)
    data = proc.stdout.decode("utf8").split()
    if data[5] == "ssid=KIT-WLAP2":
        server = "http://wwwproxy.kanazawa-it.ac.jp:8080"
        os.environ["http_proxy"] = server
        os.environ["https_proxy"] = server
        
    else:
        server = ""
        os.environ["http_proxy"] = server
        os.environ["https_proxy"] = server

'''
#学外で使用するときはこっち
server = ""
os.environ["http_proxy"] = server
os.environ["https_proxy"] = server
'''
#server = "http://wwwproxy.kanazawa-it.ac.jp:8080"
#os.environ["http_proxy"] = server
#os.environ["https_proxy"] = server

class TTS_server(object):
    def __init__(self):
        rospy.init_node('common_texttospeech')
        self.srv = rospy.Service('/tts', StrTrg, self.execute)
        rospy.loginfo("Ready to tts stdserver")
        rospy.spin()

    def execute(self, data):
        
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=data.data)
        voice = texttospeech.VoiceSelectionParams(
            language_code='en-US',
            name='en-US-Wavenet-F',
            #ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16)

        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        with open(Filename, 'wb') as out:
            out.write(response.audio_content)
            print('Audio content written to file ' + Filename)

        self.PlayWaveFile()
        return StrTrgResponse()

    def PlayWaveFile(self):
        try:
            wf = wave.open(Filename, "rb")
            print("Time[s]:", float(wf.getnframes()) / wf.getframerate())
        except FileNotFoundError:
            print("[Error 404] No such file or directory: " + Filename)
            return

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        chunk = 1024
        data = wf.readframes(chunk)
        while data != b'':
            stream.write(data)
            data = wf.readframes(chunk)
        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()
        return


if __name__ == '__main__':
    check_wifi()
    TTS_server()
    rospy.spin()
