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
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import learning_curve

class mfcc():
    def __init__(self):
        self.num = 1
        self.ls = np.array([1])
        self.mfccs_t = [np.array([-408.14777386,159.20556226,-131.47008167,117.85209979,-45.71183017,54.12468089,-60.58427186,46.25654945,-24.75584912,17.3370113,-25.22298786,19.26531063])]
        self.train_sizes = np.arange(1, 1502, 50)

    def Machine_Learning(self):
        for i in range(20):
            try:
                file_path = 'jsut_ver1_1/basic5000/wav/BASIC5000_{}.wav'.format(str(self.num).zfill(4))
                self.load_wav(file_path,1)
                file_path = 'wav2/BASIC5000_{}.wav'.format(str(self.num).zfill(4))
                self.load_wav(file_path,2)
                file_path = 'wav3/BASIC5000_{}.wav'.format(str(self.num + 600).zfill(4))
                self.load_wav(file_path,3)
            except:
                self.num = self.num + 1
        self.num = 0
        '''
        for i in range(5):
            try:
                file_path = 'wav2/BASIC5000_{}.wav'.format(str(self.num).zfill(4))
                self.load_wav(file_path,2)
            except:
                self.num = self.num + 1
        '''
        print(self.mfccs_t.shape)
        #self.load_wav('file2.wav')
        #self.load_wav('file3.wav')
        self.fitdata()
        #print(self.test('jsut_ver1_1/basic5000/wav/BASIC5000_{}.wav'.format(str(self.num ).zfill(4)),1))
        #print(self.test('file4.wav'))
        #print(self.mfccs_t[1])



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
        self.classifier = svm.SVC()#(probability=True,C=0.1)
        self.x_train,self.x_test,self.y_train,self.y_test = train_test_split(self.mfccs_t,self.ls,        test_size=0.5,random_state=0)
        #pipe = make_pipeline(StandardScaler(), SVC())
        #print(self.mfccs_t.shape,self.ls.T.shape)
        #for i in self.mfccs_t:
        #print(i)
        train_sizes, train_scores, test_scores = learning_curve(estimator=self.classifier,
                                                        X = self.mfccs_t, y = self.ls.T,
                                                        train_sizes=self.train_sizes, # 与えたデータセットの何割を使用するかを指定
                                                        cv=5, n_jobs=1)
        #print(self.ls)
        #print(train_sizes)
        #print(train_scores)
        #print(test_scores)
        #train_scores[np.isnan(train_scores)] = np.nanmean(train_scores)
        #test_scores[np.isnan(test_scores)] = np.nanmean(test_scores)
        train_mean = np.nanmean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)
        test_mean = np.nanmean(test_scores, axis=1)
        test_std = np.std(test_scores, axis=1)
        #print(train_mean,train_std,test_mean,test_std)
        plt.figure(figsize=(8,6))
        plt.plot(train_sizes, train_mean, marker='o', label='Train accuracy')
        plt.fill_between(train_sizes, train_mean + train_std, train_mean - train_std, alpha=0.2)
        plt.plot(train_sizes, test_mean, marker='s', linestyle='--', label='Validation accuracy')
        plt.fill_between(train_sizes, test_mean + test_std, test_mean - test_std, alpha=0.2)
        plt.grid()
        plt.title('Learning curve', fontsize=16)
        plt.xlabel('Number of training data sizes', fontsize=6)
        plt.ylabel('Accuracy', fontsize=6)
        plt.legend(fontsize=6)
        plt.ylim([0.3, 1.05])
        plt.xlim([0, 1800])
        plt.show()
        '''
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
        '''
        with open('sample_test.pkl','wb') as f:
            pickle.dump(self.classifier,f)
        '''
        print('finish')

        #print(self.classifier.score(self.x_test,self.y_test))

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
