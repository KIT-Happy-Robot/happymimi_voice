import sounddevice as sd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import sys
import wave
import time
import threading
import whisper
import librosa
import soundfile as sf
from sklearn import svm
import pickle

class mfcc():
    def __init__(self):
        self.num = 0
        self.ls = [10]
        self.mfccs_t = [np.full(12,0)]

    def Machine_Learning(self):
        self.load_wav('file1.wav')
        self.load_wav('file2.wav')
        self.load_wav('file3.wav')
        self.fitdata()
        #print(self.test('file4.wav'))


    def load_wav(self,file_name):
        x, fs = sf.read('./wave_file/' + file_name)
        mfccs = librosa.feature.mfcc(y = x, sr=fs,n_mfcc=12,dct_type=3)
        #print(self.mfccs_t,mfccs)
        self.mfccs_t = np.append(self.mfccs_t,mfccs.T,axis=0)
        n,data_sum = mfccs.shape
        #print(data_sum, n)
        self.ls = np.append(self.ls,np.full(data_sum,self.num))
        #print(self.ls)
        self.num += 1


    def fitdata(self):
        self.classifier = svm.SVC(probability=True, C=0.1)
        print("fit")
        self.classifier.fit( self.mfccs_t, self.ls)
        with open('fit.pkl','wb') as f:
            pickle.dump(self.classifier,f)
        print('finish')

    def test(self,file_name,num):
        x, fs = sf.read('./wave_file/' + file_name)
        mfccs = librosa.feature.mfcc(y = x, sr=fs,n_mfcc=12,dct_type=3)
        with open('fit.pkl','rb') as f:
            ls = np.full(mfccs.shape[1],num)
            self.classifier = pickle.load(f)
            data = self.classifier.score(mfccs.T,ls)
            return (data)#[0],data)


if __name__ == '__main__':
    x = mfcc()
    #x.Machine_Learning()
    print(x.test('file1.wav',0))
    print(x.test('file2.wav',1))
    print(x.test('file3.wav',2))
    print(x.test('file4.wav',2))
