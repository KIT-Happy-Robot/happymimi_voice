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
#print("now loading..")
#コサイン類似度の最小閾値
MIN_VEC = 0.5
mecab = MeCab.Tagger()
mecab.parse('')


#nltk.download('veraged_perceptron_tagger')
#word_vec = api.load("glove-twitter-200")

act_go = ["go","navigate","meet","find"]
act_tell = ["tell","introduce","speak","say"]
act_grasp = ["grasp","give","bring"]
loc = ["guest_room","kitchen","bedroom","living_room","toilet"]
tar = ["cup","bottle","tray","drink"]
hum = ["Noah","Liam","Oliver","James","Mason",
        "Olivia","Emma","Ava","Mia","Elizabeth",
        "me","boy","girl"]

prefs = ["三重","京都","佐賀","兵庫","北海道","千葉","和歌山",
        "埼玉","大分","大阪","奈良","宮城","宮崎","富山","山口","山形","山梨",
        "岐阜","岡山","岩手","島根","広島","徳島","愛媛","愛知","新潟","東京",
        "栃木","沖縄","滋賀","熊本","石川","神奈川","福井","福岡","福島","秋田",
        "群馬","茨城","長崎","長野","青森","静岡","香川","高知","鳥取","鹿児島"]
 
dates= ["今日","明日"]
types = ["天気","気温"]

w = "<nc>robot please</nc> <act>go</act> to the <location>room</location> <act>look</act> for a <human>boy</human> <act>tell</act> a <target>joke</target>"
w = "<place>大阪</place>の<date>明日</date>の<type>天気</type>を教えてください"

'''
def random_generate(root):
        buffer = ""
        pos = 0
        posdict = {}
        if len(root) == 0:
            return root.text, posdict
        
        for sentence in root:
            if sentence.tag == "act":
                act = random.choice(act_go)
                buffer += act
                posdict["act"] = (pos,pos+len(act))
                pos += len(act)

            elif sentence.tag == "location":
                location = random.choice(loc)
                buffer += location
                posdict["location"] = (pos,pos+len(location))
                pos += len(location)

            elif sentence.tag == "target":
                target = random.choice(tar)
                buffer += target
                posdict["target"] = (pos,pos+len(target))
                pos += len(target)

            elif sentence.tag == "human":
                human = random.choice(hum)
                buffer += human
                posdict["human"] = (pos,pos+len(human))
                pos += len(human)

            if sentence.tail is not None:
                buffer += sentence.tail
                pos += len(sentence.tail)

        return buffer, posdict
'''
def random_generate(root):
    buf = ""
    pos = 0
    posdic = {}
    if len(root)  == 0:
        return root.text, posdic
    
    for el in root:
        if el.tag == "place":
            pref = random.choice(prefs)
            buf += pref
            posdic["place"] = (pos, pos+len(pref))
            pos += len(pref)
        elif el.tag == "date":
            date = random.choice(dates)
            buf += date
            posdic["date"] = (pos, pos+len(date))
            pos += len(date)
        elif el.tag == "type":
            _type = random.choice(types)
            buf += _type
            posdic["type"] = (pos, pos+len(_type))
            pos += len(_type)
        if el.tail is not None:
            buf += el.tail
            pos += len(el.tail) 

    return buf, posdic  

def get_labels(POS, POSDICT):
    for label , (start, end) in POSDICT.items():
        if start <= POS and POS < end:
            return label
    return "O"

root = xml.etree.ElementTree.fromstring("<dummy>"+w+"</dummy>")
for i in range(1):
    sen, posdict = random_generate(root)
    lis = []
    pos = 0
    prev_label = 0
    #nltkを使用
    print(mecab.parse(sen))
    for line in mecab.parse(sen).splitlines():
    #for line in nltk.pos_tag(sen).splitlines():
        if line == "EOS": break
        else:
            word, feature_str = line.split("\t")
            features = feature_str.split(',')
            postag  = features[0]
            label = get_labels(pos, posdict)
            if label == "O":            lis.append([word,postag,"O"])
            elif label == prev_label:   lis.append([word,postag,"I-"+label])
            else:                       lis.append([word,postag,"B-"+label])
            pos += len(word)
            prev_label = label

for word, postag, label in lis:
    print(word + "\t" + postag + "\t" + label +"\n")