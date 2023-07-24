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
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


class mfcc():
    def __init__(self):
        self.num = 1
        self.ls = [10]
        self.mfccs_t = [np.full(12,0)]

    def Machine_Learning(self):
        for i in range(10):
            try:
                file_path = 'jsut_ver1_1/basic5000/wav/BASIC5000_{}.wav'.format(str(self.num).zfill(4))
                self.load_wav(file_path,1)
            except:
                self.num = self.num + 1
        self.num = 0
        for i in range(10):
            try:
                file_path = 'wav2/BASIC5000_{}.wav'.format(str(self.num).zfill(4))
                self.load_wav(file_path,2)
            except:
                self.num = self.num + 1
        #self.load_wav('file2.wav')
        #self.load_wav('file3.wav')
        self.fitdata()
        #print(self.test('jsut_ver1_1/basic5000/wav/BASIC5000_{}.wav'.format(str(self.num ).zfill(4)),1))
        #print(self.test('file4.wav'))


    def load_wav(self,file_name,data_num):
        x, fs = sf.read('./'+ file_name)
        mfccs = librosa.feature.mfcc(y = x, sr=fs,n_mfcc=12,dct_type=3)
        #print(self.mfccs_t,mfccs)
        self.mfccs_t = np.append(self.mfccs_t,mfccs.T,axis=0)
        n,data_sum = mfccs.shape
        #print(data_sum, n)
        self.ls = np.append(self.ls,np.full(data_sum,data_num))
        #print(self.ls)
        self.num += 1

    def fitdata(self):
        training_accuracy = []
        test_accuracy = []
        print("fit")
        self.x_train,self.x_test,self.y_train,self.y_test = train_test_split(self.mfccs_t,self.ls,test_size=0.7,random_state=0)
        for i in range(1,len(self.x_train),100):
            self.classifier = KNeighborsClassifier(n_neighbors = i)
            self.classifier.fit( self.x_train, self.y_train)
            training_accuracy.append(self.classifier.score(self.x_train,self.y_train))
            test_accuracy.append(self.classifier.score(self.x_test,self.y_test))
        plt.plot(range(1,len(self.x_train)),training_accuracy,label='Training')
        plt.plot(range(1,len(self.x_test)),test_accuracy,label='Test')
        plt.ylabel('A')
        plt.xlabel('n_')
        plt.legend()
        '''
        with open('sample_test.pkl','wb') as f:
            pickle.dump(self.classifier,f)
        '''
        print('finish')

        print(self.classifier.score(self.x_test,self.y_test))

    def test(self,file_name,num):
        x, fs = sf.read('./' + file_name)
        mfccs = librosa.feature.mfcc(y = x, sr=fs,n_mfcc=12,dct_type=3)
        ls = np.full(mfccs.shape[1],num)
        data = self.classifier.score(mfccs.T,ls)
        return (data)

    def pkltest(self,file_name,num):
        x, fs = sf.read('./' + file_name)
        mfccs = librosa.feature.mfcc(y = x, sr=fs,n_mfcc=12,dct_type=3)
        with open('sample_test.pkl','rb') as f:
            ls = np.full(mfccs.shape[1],num)
            self.classifier = pickle.load(f)
            data = self.classifier.score(mfccs.T,ls)
            return (data)#[0],data)


if __name__ == '__main__':
    x = mfcc()
    x.Machine_Learning()
    '''
    ls = []
    for i in range(500):
        try:
            ls.append(x.pkltest('jsut_ver1_1/basic5000/wav/BASIC5000_{}.wav'.format(str(i).zfill(4)),1))
            ls.append(x.pkltest('wav2/BASIC5000_{}.wav'.format(str(i).zfill(4)),2))
        except:
            continue
    print((sum(ls)/len(ls)))
    '''
    #print(x.test('file1.wav',0))
    #print(x.test('file2.wav',1))
    #print(x.test('file3.wav',2))
    #print(x.test('file4.wav',2))
