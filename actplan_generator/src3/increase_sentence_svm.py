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
from pymagnitude import Magnitude

file_path=path.expanduser('~/ros1_ws/src/happymimi_voice/config')
#ベクトル読み込み
print("now loading..")
#コサイン類似度の最小閾値
MIN_VEC = 0.5

#nltk.download('veraged_perceptron_tagger')
#word_vec = api.load("glove-twitter-200")
vectors = Magnitude("/home/kouya/Downloads/crawl-300d-2M.magnitude")

class Increase_Sentence():
    def __init__(self):
        
        self.act_go = ["go","navigate","meet","find"]
        self.act_navigate = ["navigate","escort","guide"]
        self.act_tell = ["tell","introduce","speak","say"]
        self.act_grasp = ["grasp","give","bring"]

        self.location = ["guest_room","kitchen","bedroom","living_room","toilet"]
        self.tar_object = ["cup","bottle","tray","drink","bowl","cloth"]
        self.tar_do = ["joke","day","month"]
        self.tar_human = ["boy","people","everyone"]
        self.human = ["Noah","Liam","Oliver","James","Mason",
                      "Olivia","Emma","Ava","Mia","Elizabeth",
                      "me","boy","girl"]

        #self.dataset_path = dataset_path
        #self.dataset = dataset
        self.pos = 0
        self.posdict = {}

    def compare_similarity_action(self,word):
        word_list = ["go","navigate","tell","grasp"]
        word_dict = {}
        result = []
        max_value = []
        for i in range(len(word_list)):
            result.append(vectors.similarity(word,word_list[i]))
            word_dict[word_list[i]] = result[i]
            
        #print(word_dict)
        max_key = max(word_dict.items(), key = lambda x:x[1])
        return max_key[0]
        

    def compare_similarity_target(self,word):
        word_list = ["object","day","human"]
        word_dict = {}
        result = []
        max_value = []
        for i in range(len(word_list)):
            result.append(vectors.similarity(word,word_list[i]))
            word_dict[word_list[i]] = result[i]
            
        #print(word_dict)
        max_key = max(word_dict.items(), key = lambda x:x[1])
        return max_key[0]


    def get_label(self, pos, posdic):
        for label, (start, end) in posdic.items():
            if start <= pos and pos < end:
                #print(label)
                return label
        return "O"

    def split_and_pos(self, sen):
        morph = nltk.word_tokenize(sen)   #分かち書き)
        pos =  nltk.pos_tag(morph) #品詞の取得
        #print(pos)
        #print(a)
        
        return pos

    #ランダムで文章を生成する
    def random_generate(self, root):
            buffer = ""
            pos = 0
            num_act = 1
            num_loc = 1
            num_tar = 1
            num_hum = 1
            posdict = {}
            if len(root) == 0:
                return root.text, posdict
            
            for sentence in root:
                if sentence.tag == "act":
                    if self.compare_similarity_action(sentence.text) == 'go': 
                        act = random.choice(self.act_go)
                    elif self.compare_similarity_action(sentence.text) == 'navigate':
                        act = random.choice(self.act_navigate)
                    elif self.compare_similarity_action(sentence.text) == 'tell':
                        act = random.choice(self.act_tell)
                    elif self.compare_similarity_action(sentence.text) == 'grasp':
                        act = random.choice(self.act_grasp)

                    buffer += act
                    if "act_0" in posdict:
                        posdict["act_"+ str(num_act)] = (pos,pos+len(act))
                        num_act += 1
                    
                    else:
                        posdict["act_0"] = (pos,pos+len(act))
                    pos += len(act)

                elif sentence.tag == "location":
                    location = random.choice(self.location)
                    buffer += location
                    if "location_0" in posdict:
                        posdict["location_"+ str(num_loc)] = (pos,pos+len(location))
                        num_loc += 1
                        
                    else:
                        posdict["location_0"] = (pos,pos+len(location))
                    pos += len(location)

                                        
                elif sentence.tag == "target":
                    if self.compare_similarity_target(sentence.text) == 'object':
                        target = random.choice(self.tar_object)
                    elif self.compare_similarity_target(sentence.text) == 'day':
                        target = random.choice(self.tar_do)
                    elif self.compare_similarity_target(sentence.text) == 'human':
                        target = random.choice(self.tar_human)
                    
                    buffer += target
                    if "target_0" in posdict:
                        posdict["target_"+ str(num_tar)] = (pos,pos+len(target))
                        num_tar += 1
                        
                    else:
                        posdict["target_0"] = (pos,pos+len(target))
                    pos += len(target)

                elif sentence.tag == "human":
                    human = random.choice(self.human)
                    buffer += human
                    if "human_0" in posdict:
                        posdict["human_"+ str(num_hum)] = (pos,pos+len(human))
                        num_hum += 1
                        
                    else:
                        posdict["human_0"] = (pos,pos+len(human))
                    pos += len(human)

                elif sentence.tag == "nc":
                    buffer += sentence.text
                    #print(sentence.text)
                    pos += len(sentence.text)

                if sentence.tail is not None:
                    buffer += sentence.tail
                    pos += len(sentence.tail)

                #print(sentence)

            return buffer, posdict

    def execute(self):
        da = " "
        cnt = 0
        f = open("svm_sentences.dat","w")
        for line in open("exam_svm.txt", "r"):
            line  = line.strip()
            if re.search(r'^da=', line):
                da = line.replace('da=', '')
            elif line == "":
                pass
            else:
                cnt += 1
                print(cnt,":",line)
                root = xml.etree.ElementTree.fromstring("<dummy>"+line+"</dummy>")
                
                for i in range(100):
                    sen, posdict = self.random_generate(root)
                    lis = []
                    pos = 0
                    prev_label = 0
                    line = self.split_and_pos(sen)
                    #print("posdict:",posdict)
            
                    f.write(da + "\t" + sen +"\n")
                f.write("\n")
        
        print("finish increase")
        f.close()
        

if __name__ == "__main__":
    incse = Increase_Sentence()
    incse.execute()
