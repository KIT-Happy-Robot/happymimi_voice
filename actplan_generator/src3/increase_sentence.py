#!/usr/bin/env python3                                                      
# -*- coding: utf-8 -*-
import numpy
import sys
from os import path
import re
import random
import xml.etree.ElementTree
import MeCab
import nltk

#from gensim.models import KeyedVectors
import gensim.downloader as api

file_path=path.expanduser('~/ros1_ws/src/happymimi_voice/config')
#ベクトル読み込み
print("now loading..")
#コサイン類似度の最小閾値
MIN_VEC = 0.5

#nltk.download('veraged_perceptron_tagger')
word_vec = api.load("glove-twitter-200")


class Increase_Sentence():
    def __init__(self, dataset_path="../resource/",
                 dataset = "crf_str.txt"):
        
        self.act_go = ["go","navigate","meet","find"]
        self.act_tell = ["tell","introduce","speak","say"]
        self.act_grasp = ["grasp","give","bring"]

        self.location = ["guest_room","kitchen","bedroom","living_room","toilet"]
        self.target = ["cup","bottle","tray","drink"]
        self.human = ["Noah","Liam","Oliver","James","Mason",
                      "Olivia","Emma","Ava","Mia","Elizabeth",
                      "me","boy","girl"]

        self.dataset_path = dataset_path
        self.dataset = dataset
        self.pos = 0
        self.posdict = {}

    def random_generate(self, root):
        buffer = ""
        pos = 0
        posdict = {}
        if len(root) == 0:
            return root.text, posdict
        
        for sentence in root:
            if sentence.tag == "act":
                act = random.choice(self.act_go)
                buffer += act
                posdict["act"] = (pos,pos+len(act))
                pos += len(act)

            elif sentence.tag == "location":
                location = random.choice(self.location)
                buffer += location
                posdict["location"] = (pos,pos+len(location))
                pos += len(location)

            elif sentence.tag == "target":
                target = random.choice(self.target)
                buffer += target
                posdict["target"] = (pos,pos+len(target))
                pos += len(target)

            elif sentence.tag == "human":
                human = random.choice(self.human)
                buffer += human
                posdict["human"] = (pos,pos+len(human))
                pos += len(human)

            if sentence.tail is not None:
                buffer += sentence.tail
                pos += len(sentence.tail)

        return buffer, posdict
                

    def get_labels(self, POS, POSDICT):
        for label , (start, end) in POSDICT.items():
            if start <= POS and POS < end:
                return label
        return "O"
    
    def execute(self):
        f = open("crf_sentence.dat", "w")
        for line in open(self.dataset_path+self.dataset, "r"):
            line  = line.strip()
            if re.search(r'^da=', line):
                da = line.replace('da=', '')
            elif line == "":
                pass
            else:
                root = xml.etree.ElementTree.fromstring("<dummy>"+line+"</dummy>")
                for i in range(10):
                    sen, posdict = self.random_generate(root)
                    lis = []
                    pos = 0
                    prev_label = 0
                    #nltkを使用
                    for line in nltk.pos_tag(sen).splitlines():
                        if line == "EOS": break
                        else:
                            word, feature_str = line.split("\t")
                            features = feature_str.split(',')
                            postag  = features[0]
                            label = self.get_labels(pos, posdict)
                            if label == "O":            lis.append([word,postag,"O"])
                            elif label == prev_label:   lis.append([word,postag,"I-"+label])
                            else:                       lis.append([word,postag,"B-"+label])
                            pos += len(word)
                            prev_label = label

            for word, postag, label in lis:
                f.write(word + "\t" + postag + "\t" + label +"\n")
            f.write("\n")

if __name__ == "__main__":
    incse = Increase_Sentence()
    incse.execute()
