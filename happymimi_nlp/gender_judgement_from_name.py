# !/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
#import pickle as pk
import dill
from nltk.corpus import names
import random
import math
import os.path
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


if __name__ == '__main__':
    classifier=GenderJudgementFromNameByNBC.trainNBCmodel()
    classifier.confirmAccuracy()

    while 1:
        i=input("name or save:")
        if(i=="save"):
            classifier.save()
        else:
            print(classifier.expectGender(i))
