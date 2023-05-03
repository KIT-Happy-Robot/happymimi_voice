import whisper
import pyaudio
import wave

record_secound = 10
wave_filename = "sample_pyaudio.wav"
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

MakeWavFile(wave_filename, Record_Seconds = 5)
model = whisper.load_model("small")
result = model.transcribe(wave_filename, verbose=False, language="en")
print(result["text"])
