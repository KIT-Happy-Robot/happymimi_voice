#! /usr/bin/env python
# -*- coding: utf-8 -*-

# [START speech_transcribe_streaming_mic]
from __future__ import division

import re
import sys
import rospy
from happymimi_voice_msgs.srv import SpeechToText
from happymimi_voice_msgs.srv import SpeechToTextResponse
#import actionlib
from google.cloud import speech_v1p1beta1 as speech
#from google.cloud.speech import enums 消えたらしい
#from google.cloud.speech import types
import roslib.packages
happymimi_voice_path=roslib.packages.get_pkg_dir("happymimi_voice")+"/../config/wave_data/PI.wav"
import pyaudio
from six.moves import queue
import wave
import pyaudio

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

class speech_server():
    def __init__(self):
        print('server is ready')
        self.server=rospy.Service('/stt_server2',SpeechToText,self.google_speech_api)

    def listen_print_loop(self,responses):
        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

        # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
            #print(transcript + overwrite_chars)
                sys.stdout.write(transcript + overwrite_chars + '\r')
                sys.stdout.flush()

                num_chars_printed = len(transcript)

            else:
                print(transcript + overwrite_chars)
                break

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
                if re.search(r'\b(exit|quit)\b', transcript, re.I):
                    print('Exiting..')
                    break
                num_chars_printed = 0
        return (transcript + overwrite_chars).lower()

    def google_speech_api(self,req):
        language_code = 'en-US'
        if req.short_str:
            speech_contexts_element = speech.SpeechContext(phrases=req.context_phrases)
            #print(speech_contexts_element)
            client = speech.SpeechClient()

            metadatas = speech.RecognitionMetadata()
            metadatas.microphone_distance = (
                        speech.RecognitionMetadata.MicrophoneDistance.NEARFIELD)#NEARFIELD  MIDFIELDはマイクがスピーカから３メートル以内
            metadatas.interaction_type = (
                        speech.RecognitionMetadata.InteractionType.VOICE_COMMAND)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=RATE,
                language_code=language_code,
                speech_contexts=[speech_contexts_element],
                model='command_and_search',
                metadata=metadatas)
        else:
            client = speech.SpeechClient()

            metadatas = speech.RecognitionMetadata()
            metadatas.microphone_distance = (
                        speech.RecognitionMetadata.MicrophoneDistance.NEARFIELD)#NEARFIELD  MIDFIELDはマイクがスピーカから３メートル以内
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=RATE,
                language_code=language_code,
                metadata=metadatas,
                enable_automatic_punctuation=True)

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

        try:
            wf = wave.open(happymimi_voice_path, "rb")
            print("Time[s]:", float(wf.getnframes()) / wf.getframerate())
        except FileNotFoundError:
            pass
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

        with MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (speech.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = client.streaming_recognize(streaming_config, requests)
            return SpeechToTextResponse(result_str=self.listen_print_loop(responses))


if __name__=='__main__':
    rospy.init_node('stt_server2')
    f=speech_server()
    rospy.spin()
