#!/usr/bin/env python3                                                      
# -*- coding: utf-8 -*-
import numpy
import sys
from os import path
import re
import random
from pprint import pprint

import xml.etree.ElementTree
import MeCab
import nltk


from pymagnitude import Magnitude

mecab = MeCab.Tagger()
mecab.parse('')
print("now_loading...")
vectors = Magnitude("/home/kouya/Downloads/crawl-300d-2M.magnitude")

#w = "<nc>robot please</nc> <act>go</act> to the <location>room</location> <act>look</act> for a <human>boy</human> <act>tell</act> a <target>joke</target>"
#w = "<nc>could you</nc> <act>tell</act> <human>me</human> how many <target>people</target> in the <location>room</location> are"
w = "<act>go</act> to the <location>location</location> <act>find</act> the <target>tray</target> <act>give</act> it to <human>name</human> at the <location>location</location>"


act_go = ["go","move","pass"]
act_navigate = ["navigate","escort","guide"]
act_tell = ["tell","introduce","speak","say","contact","meet","find"]
act_grasp = ["grasp","give","bring","get","place"]

loc = ["guest_room","kitchen","bedroom","living_room","toilet"]

tar_object = ["cup","bottle","tray","drink","bowl","cloth"]
tar_do = ["joke","day","month"]
tar_human = ["boy","people","everyone"]

hum = ["Noah","Liam","Oliver","James","Mason",
        "Olivia","Emma","Ava","Mia","Elizabeth",
        "me","boy","girl"]

def compare_similarity_action(word):
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
          

def compare_similarity_target(word):
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


def get_label(pos, posdic):
    for label, (start, end) in posdic.items():
        if start <= pos and pos < end:
            return label
    return "O"

      
def random_generate(root):
        buffer = ""
        pos = 0
        posdict = {}
        num_act = 0
        num_loc = 0
        num_tar = 0
        num_hum = 0
        
        if len(root) == 0:
            return root.text, posdict
        
        for sentence in root:
            if sentence.tag == "act":
                if compare_similarity_action(sentence.text) == 'go': 
                     act = random.choice(act_go)
                elif compare_similarity_action(sentence.text) == 'navigate':
                     act = random.choice(act_navigate)
                elif compare_similarity_action(sentence.text) == 'tell':
                     act = random.choice(act_tell)
                elif compare_similarity_action(sentence.text) == 'grasp':
                     act = random.choice(act_grasp)

                buffer += act 
                
                posdict["act"] = (pos,pos+len(act))
                pos += len(act)

            elif sentence.tag == "location":
                location = random.choice(loc)
                buffer += location
                posdict["location"] = (pos,pos+len(location))
                pos += len(location)

            elif sentence.tag == "target":
                if compare_similarity_target(sentence.text) == 'object':
                    target = random.choice(tar_object)
                elif compare_similarity_target(sentence.text) == 'day':
                    target = random.choice(tar_do)
                elif compare_similarity_target(sentence.text) == 'human':
                    target = random.choice(tar_human)
                
                buffer += target
                posdict["target"] = (pos,pos+len(target))
                pos += len(target)

            elif sentence.tag == "human":
                human = random.choice(hum)
                buffer += human
                posdict["human"] = (pos,pos+len(human))
                pos += len(human)

            elif sentence.tag == "nc":
                 buffer += sentence.text
                 pos += len(sentence)

            if sentence.tail is not None:
                buffer += sentence.tail
                pos += len(sentence.tail)

            #print(sentence)

        return buffer, posdict

def main():
    cnt = 0
    f = open("crf_sentences.dat","w")
    for line in open("exam.txt", "r"):
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
                sen, posdict = random_generate(root)
                lis = []
                pos = 0
                prev_label = 0
                for line in mecab.parse(sen).splitlines():
                    if line == "EOS": break
                      
                    else:
                        
                        word, feature_str = line.split("\t")
                        features = feature_str.split(',')
                        postag  = features[0]
                        label = get_label(pos, posdict)
                        if label == "O":
                            lis.append([word,postag,"O"])
                        elif label == prev_label:
                            lis.append([word,postag,"I-"+label])
                        else:
                            lis.append([word,postag,"B-"+label])
                        
                        pos += len(word)
                        prev_label = label

            for word, postag, label in lis:
                f.write(word + "\t" + postag + "\t" + label +"\n")
            f.write("\n")
    
    print("finish increase")
    f.close()
    #print(sen)

if __name__ == "__main__":
    #root = xml.etree.ElementTree.fromstring("<dummy>"+w+"</dummy>")
    #sen, posdict = random_generate(root)
    #print(sen)
    main()