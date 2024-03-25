#!/usr/bin/env python3

import pyaudio
import sys
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
import wave
import rospy
import roslib
from happymimi_msgs.srv import SetStr, SetStrResponse


#pi_sound
happymimi_voice_path=roslib.packages.get_pkg_dir("happymimi_voice")
sound_path = "/../config/wave_data/PI.wav"
sys.path.insert(0,happymimi_voice_path+"/src")
from whisper_stt import Whisper_Stt

class Distil_Whisper_Stt(Whisper_Stt):
    def __init__(self):
        super().__init__()
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model_id = "distil-whisper/distil-large-v3"
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_id, torch_dtype=self.torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        self.model.to(self.device)

        self.processor = AutoProcessor.from_pretrained(self.model_id)

        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            max_new_tokens=128,
            torch_dtype=self.torch_dtype,
            device=self.device,
        )
        
        rospy.loginfo("distil_whisper_ready")
        self.srv = rospy.Service("/distil_whisper_stt",SetStr,self.distil_whisper_server)
        
    def distil_whisper_server(self,_):
        self.MakeWavFile()
        result = self.pipe(self.wave_filename)
        print(result["text"])
        
        return SetStrResponse(result = result["text"])
    
if __name__ == "__main__":    
    rospy.init_node("distil_whisper_stt")
    dws = Distil_Whisper_Stt()
    rospy.spin()