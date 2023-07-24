#!/usr/bin/env python3                                                      
# -*- coding: utf-8 -*-
#import sklearn_crfsuite
#from crf_util import word2fetures, sent2features, sent2labels
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill 
import nltk
from increase_sentence_crf import Increase_Sentence

SENTS = []
LIS = []
MODEL_PATH = "../resource/src3/"

def train_crf(SENTS,LIS):
    for line in open("svm_sentences.dat", "r"):
        line = line.rstrip()
        lines = line.split('\t')
        #print(lines)
        if lines == ['']:
            #print(lines)
            pass
        else:
            da = lines[0]
            utt = lines[1]

            words = []
            sentence = module.split_and_pos(utt)
            for i in range(len(sentence)):
                if i == "EOS":
                    break
                else:
                    word = sentence[i][0]
                    feature_str = sentence[i][1]
                    words.append(word)
        SENTS.append(" ".join(words))
        LIS.append(da)
    #print(SENTS)
    vectorizer = TfidfVectorizer(tokenizer=lambda x:x.split())    
    X = vectorizer.fit_transform(SENTS)
    
    label_encoder = LabelEncoder()
    Y = label_encoder.fit_transform(LIS)
    
    svc = SVC(gamma="scale")
    svc.fit(X,Y)
    
    with open(MODEL_PATH+"svc.model", "wb") as f:
        dill.dump(vectorizer, f)
        dill.dump(label_encoder,f)
        dill.dump(svc, f)
        #for line in mecab.parse(source, filename='', mode='exec'):

if __name__ == "__main__":
    module = Increase_Sentence()
    train_crf(SENTS,LIS)