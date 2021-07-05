#!/usr/bin/env python
# -*- cording: utf-8 -*-


import pyaudio
import wave
import rospy
from std_srvs.srv import Empty
from std_srvs.srv import EmptyResponse


file='/home/athome/catkin_ws/src/ggi/one33.wav'

class call:
    def __init__(self):
        rospy.init_node("sound_effect",anonymous=True)
        print("server is ready")
        server=rospy.Service('/sound',Empty,self.run_quickstart)

    def run_quickstart(self,req):
        wf = wave.open(file, 'rb')

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)

        chunk = 1024
        data = wf.readframes(chunk)
        while len(data)>0:
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()

        return EmptyResponse()


if __name__=='__main__':
    call()
    rospy.spin()
