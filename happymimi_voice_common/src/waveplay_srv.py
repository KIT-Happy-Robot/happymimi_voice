#!/usr/bin/env python
#-*- coding: utf-8 -*-

import roslib
import rospy
from happymimi_msgs.srv import StrTrg,StrTrgResponse
from google.cloud import texttospeech
import wave
import pyaudio

#Filename = 'output.wav'
file_path=roslib.packages.get_pkg_dir("happymimi_voice")+"/../config/wave_data"

class WavePlay():
    def __init__(self):

        self.srv = rospy.Service('/waveplay_srv', StrTrg, self.PlayWaveFile)
        rospy.spin()


    def PlayWaveFile(self,file_name):
        try:
            wf = wave.open(file_path+file_name.data, "rb")
            print("Time[s]:", float(wf.getnframes()) / wf.getframerate())
        except FileNotFoundError:
            print("[Error 404] No such file or directory: " + file_name.data)
            return StrTrgResponse(result=False)

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
        p.terminate()
        wf.close()
        return StrTrgResponse(result=True)

def waveMake(sentence,file_name):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=sentence)
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Wavenet-F',
        #ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open(file_path+file_name, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file ' + file_name)

def PlayWaveFile(file_name):
    try:
        wf = wave.open(file_path+file_name, "rb")
        print("Time[s]:", float(wf.getnframes()) / wf.getframerate())
    except FileNotFoundError:
        print("[Error 404] No such file or directory: " + file_name)
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
    p.terminate()
    return

if __name__ == '__main__':
    rospy.init_node('waveplay_srv')
    WavePlay()
