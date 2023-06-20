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
MODEL_PATH = "../resource/src3/"
#nltk.download('veraged_perceptron_tagger')
#word_vec = api.load("glove-twitter-200")
vectors = Magnitude("/home/kouya/Downloads/crawl-300d-2M.magnitude")

example_sentence1 = "<act>Get</act> the <target>bowl</target> from the <location>chair</location> and <act>put</act> <target>it<target> on the <location>shelf</location>"
example_sentence2 = "<act>Follow</act> <human>Mary</human>"
example_sentence3 = "<act>Meet</act> <human>Jennifer</human> at the <location>desk</location>, <act>follow</act> <human>her</human>, and <act>accompany</act> <human>her</human> back" 

class Increase_Sentence():
    def __init__(self):
        
        self.act_go = ["go","meet","find","contact","face","locate"]
        self.act_navigate = ["navigate","escort","guide","accompany","follow","contact","lead"]
        self.act_tell = ["tell","introduce","speak","say","ask","answer"]
        self.act_grasp = ["get","grasp","give","bring","put",
                          "serve","pick","deliver","provide","take"]

        self.location = ["guest-room","kitchen","bed room","living-room","cab",
                         "toilet","operator","desk","shelf","chair","entrance","table"]
        
        self.tar_object = ["cup","blue cup","three cups",
                           "bottle","two bottle","red bottle",
                           "tray","drinks","bowl","cloth"]
        
        ##ここのところは水増しの方法を変えるべきかな
        #しゃべる内容など
        self.tar_day = ["joke","day","month","week"]
        
        #見る対象
        self.tar_human = ["gender of the person","how many people","name fo the person",
                          "person pointing to the right","person pointing to the left",
                          "person waving hand"]
        ##
        
        ##人名とか、[person pointing to the left]にも対応する必要があり
        self.human = ["Noah","Liam","Oliver","James","Mason",
                      "Olivia","Emma","Ava","Mia","Elizabeth",
                      "Skyler","Alex","Patricia","John","Jack"]
        
        self.human_other = ["everyone","him","her","me","woman","man"]
        
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
                        #target = random.choice(self.tar_object)
                        pass
                    elif self.compare_similarity_target(sentence.text) == 'day':
                        #target = random.choice(self.tar_do)
                        pass
                    elif self.compare_similarity_target(sentence.text) == 'human':
                        #target = random.choice(self.tar_human)
                        pass
                    
                    target = sentence.text
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
        
    def random_execute_fix(self, root):
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
        cnt = 0
        f = open(MODEL_PATH+"crf_sentences.dat","w")
        for line in open(MODEL_PATH+"input_str_ver2.txt", "r"):
            line  = line.strip()
            if re.search(r'^da=', line):
                da = line.replace('da=', '')
            elif line == "":
                pass
            else:
                cnt += 1
                print(cnt,":",line)
                root = xml.etree.ElementTree.fromstring("<dummy>"+line+"</dummy>")
                
                for i in range(1000):
                    sen, posdict = self.random_generate(root)
                    lis = []
                    pos = 0
                    prev_label = 0
                    line = self.split_and_pos(sen)
                    #print("posdict:",posdict)
                    for j in range(len(line)):
                        
                        word = line[j][0]
                        postag = line[j][1]
                        label = self.get_label(pos, posdict)
                        #print("pos:",pos,"word:",word)
                        if label == "O":
                            lis.append([word,postag,"O"])
                        elif label == prev_label:
                            lis.append([word,postag,"I-"+label])
                        else:
                            lis.append([word,postag,"B-"+label])
                                    
                        pos += len(word)
                        pos += 1
                        prev_label = label

                for word, postag, label in lis:
                    f.write(word + "\t" + postag + "\t" + label +"\n")
                f.write("\n")
        
        print("finish increase")
        f.close()
        
        def sample_execute(self):
            line1 = example_sentence1
            line2 = example_sentence2
            line3 = example_sentence3
            
            root = xml.etree.ElementTree.fromstring("<dummy>"+line1+"</dummy>")
            
            for i in range(1):
                sen, posdict = self.random_generate(root)
                print(sen)
                lis = []
                pos = 0
                prev_label = 0
                '''
                line = self.split_and_pos(sen)
                #print("posdict:",posdict)
                for j in range(len(line)):
                    
                    word = line[j][0]
                    postag = line[j][1]
                    label = self.get_label(pos, posdict)
                    #print("pos:",pos,"word:",word)
                    if label == "O":
                        lis.append([word,postag,"O"])
                    elif label == prev_label:
                        lis.append([word,postag,"I-"+label])
                    else:
                        lis.append([word,postag,"B-"+label])
                                
                    pos += len(word)
                    pos += 1
                    prev_label = label
                '''
        
if __name__ == "__main__":
    incse = Increase_Sentence()
    incse.execute()
