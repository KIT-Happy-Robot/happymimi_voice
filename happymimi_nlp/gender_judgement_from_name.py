# !/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
#import pickle as pk
import dill
from nltk.corpus import names
import numpy as np
import random
import math
import os.path
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import StackingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
import ngram

#pickleだとlambdaでエラーが出るためdillを使う
def dillWrite(file_path,data):
    with open(file_path,"wb") as f:
        dill.dump(data,f)
    print("save for "+file_path)

def dillLoad(file_path):
    with open(file_path,"rb") as f:
        data=dill.load(f)
    print("load from "+file_path)
    return data

class GenderJudgementFromNameByNBC:
    def __init__(self,classifier,gender_features,test_set1,test_set2):
        self.classifier=classifier
        self.gender_features=gender_features
        self.test_set1=test_set1
        self.test_set2=test_set2

    def confirmAccuracy(self):
        print("test1 : "+str(nltk.classify.accuracy(self.classifier,self.test_set1)))
        print("test2 : "+str(nltk.classify.accuracy(self.classifier,self.test_set2)))

    def expectGender(self,name):
        return self.classifier.classify(self.gender_features(name.lower()))


    def save(self,file_path="./genderNBCmodel.dill"):
        dillWrite(file_path,{'model':self.classifier,'features':self.gender_features,
                        'test1':self.test_set1,'test2':self.test_set2})


    @classmethod
    def loadNBCmodel(cls,file_path="./genderNBCmodel.dill"):
        if(os.path.exists(file_path)):
            data=dillLoad(file_path)
            return cls(data['model'],data['features'],data['test1'],data['test2'])
        else:
            print("No such file")
            return None

    @classmethod
    def trainNBCmodel(cls,first_num=2,midle_num=1,last_num=1):
        names_data= ([(name.lower() , 'male') for name in names.words('male.txt')] + \
            [(name.lower(), 'female') for name in names.words('female.txt')])
        random.shuffle(names_data)
        gender_features=lambda word: {'last_letter':word[-last_num:],
                                    'middle_letter':word[math.floor(len(word)/2):math.floor(len(word)/2)+midle_num],
                                    'first_letter':word[:first_num]}
        featuresets=[(gender_features(n), g) for (n, g) in names_data]
        train_set,test_set,st_set=featuresets[1000:],featuresets[:500],featuresets[500:1000]

        classifier = nltk.NaiveBayesClassifier.train(train_set)

        return cls(classifier,gender_features,test_set,st_set)


#スタッキングを使ったやつ　結果：精度はナイーブベイズのが上
class GenderJudgementFromNameByStacking:
    def __init__(self,classifier,gender_features,test_set1,test_set2):
        self.classifier=classifier
        self.gender_features=gender_features
        self.test_set1=test_set1
        self.test_set2=test_set2

    def confirmAccuracy(self):
        print("test1 : "+str(self.classifier.score(self.test_set1[0], self.test_set1[1])))
        print("test2 : "+str(self.classifier.score(self.test_set2[0], self.test_set2[1])))

    def expectGender(self,name):
        if self.self.classifier.predict(np.array(self.gender_features(name.lower()))):
            return "female"
        else :
            return "male"


    def save(self,file_path="./genderStackingmodel.dill"):
        dillWrite(file_path,{'model':self.classifier,'features':self.gender_features,
                        'test1':self.test_set1,'test2':self.test_set2})


    @classmethod
    def loadNBCmodel(cls,file_path="./genderStackingmodel.dill"):
        if(os.path.exists(file_path)):
            data=dillLoad(file_path)
            return cls(data['model'],data['features'],data['test1'],data['test2'])
        else:
            print("No such file")
            return None

    @classmethod
    def trainStackingmodel(cls,first_num=2,midle_num=1,last_num=1,max_iter1=1000,max_iter2=10000):

        def gender_features(word):
            x_sub=[]
            for num,i in enumerate(word[-last_num:]):
                x_sub.append(chr_dict[i])
            for num,i in enumerate(word[math.floor(len(word)/2):math.floor(len(word)/2)+midle_num]):
                x_sub.append(chr_dict[i])
            for num,i in enumerate(word[:first_num]):
                x_sub.append(chr_dict[i])
            return x_sub
        '''
        def gender_features(word):
            x_sub=[]
            for i in index.ngrams(word):
                x_sub.append(ngram_dict[i])

            for i in range(len(x_sub),max_len):
                x_sub.append(0)

            return x_sub
        '''


        names_data= ([(name.lower() , 'male') for name in names.words('male.txt')] + \
            [(name.lower(), 'female') for name in names.words('female.txt')])
        random.shuffle(names_data)
        index = ngram.NGram(N=2)
        #max_len=max([len(list(index.ngrams(n))) for (n,g) in names_data])
        x=[]
        y=[]
        #chr_ls=[chr(i) for num,i in enumerate(range(97, 97+26))]
        chr_dict={chr(i):i for num,i in enumerate(range(97, 97+26))}
        chr_dict["-"]=26
        chr_dict[" "]=27
        chr_dict["'"]=28
        '''
        id=0
        ngram_dict={}
        for i in chr_ls:
            for t in chr_ls:
                id+=1
                ngram_dict[i+t]=id
        '''
        gender_dict={"male":0,"female":1}
        for n,g in names_data:
            x.append(gender_features(n))
            y.append(gender_dict[g])

        #print([len(i) for i in x])
        x=np.array(x)
        y=np.array(y)
        x_train,y_train,x_test1,y_test1,x_test2,y_test2=(x[1000:],y[1000:],x[:500],y[:500],x[500:1000],y[500:1000])
        estimators = [
        ('svc', make_pipeline(StandardScaler(), SVC())),
        ('rf', RandomForestClassifier()),
        ('clf', GaussianNB())
        ]
        classifier = StackingClassifier(
            estimators=estimators,
            final_estimator=LogisticRegression(max_iter=max_iter2)
        )
        classifier.fit(x_train, y_train)

        return cls(classifier,gender_features,(x_test1,y_test1),(x_test2,y_test2))




if __name__ == '__main__':
    classifier=GenderJudgementFromNameByStacking.trainStackingmodel()
    classifier.confirmAccuracy()

    while 1:
        i=input("name or save:")
        if(i=="save"):
            classifier.save()
        else:
            print(classifier.expectGender(i))
