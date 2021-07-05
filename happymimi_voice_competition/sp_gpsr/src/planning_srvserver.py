#!/usr/bin/env python
#-*- coding: utf-8 -*-

import roslib
import rospy
from gcp_speech_recognition.srv import SpeechRecog
from gcp_texttospeech.srv import TTS
from gpsr.srv import ActionPlan
from gpsr.srv import ActionPlanResponse

import lp_gpsr

tts_pub = rospy.ServiceProxy('/tts', TTS)
stt_pub = rospy.ServiceProxy('/speech_recog', SpeechRecog)
lp = lp_gpsr.GPSR_data()

def speak(sentence):
    tts_pub(sentence)
    return

def speech_recog():
    return stt_pub()

def control(_dammy):
    plan = ActionPlanResponse()
    tmp_array = []
    recog_result = speech_recog()
    print(recog_result)
    lp_result = lp.FixSentence(recog_result.result)

    if lp_result == 'ERROR':
        rospy.loginfo('WARNING: rocognition result is too bad')
        # speak("one more time please")
        plan.result = False

    else:
        rospy.loginfo('Succeced speech recognition')
        speak(lp_result)
        plan.result = True
        tmp_array = lp.MakeAction()
        tmp_action = []
        tmp_data = []

        print(tmp_array)

        for i in tmp_array:
            if i[0] == "end":
                break

            tmp_action.append(i[0])

            for j in range(1, 3):
                if i[j] == "none":
                    pass
                else:
                    print(i[j])
                    tmp_data.append(i[j])
                    break

        plan.action = tmp_action
        plan.data = tmp_data

    print(plan.action)
    print(plan.data)
    return plan


def main():
    rospy.init_node('gpsr_action_planning')
    srv = rospy.Service('/gpsr/actionplan',ActionPlan ,control)
    rospy.loginfo('Ready to gpsr planning_srvserver')
    rospy.spin()

if __name__=='__main__':
    main()
