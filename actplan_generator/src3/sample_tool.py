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
print("now_loading...")
vectors = Magnitude("/home/kouya/Downloads/crawl-300d-2M.magnitude")

#from gensim.models import KeyedVectors
#import gensim.downloader as api

results = vectors.most_similar(u'go', topn = 10)

# resultsを表示。
for result in results:
    print(result)

w = "<nc>robot please</nc> <act>go</act> to the <location>room</location> <act>look</act> for a <human>boy</human> <act>tell</act> a <target>joke</target>"

act_go = ["go","navigate","meet","find"]
act_tell = ["tell","introduce","speak","say"]
act_grasp = ["grasp","give","bring"]
loc = ["guest_room","kitchen","bedroom","living_room","toilet"]
tar = ["cup","bottle","tray","drink"]
hum = ["Noah","Liam","Oliver","James","Mason",
        "Olivia","Emma","Ava","Mia","Elizabeth",
        "me","boy","girl"]


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

            elif sentence.tag == "nc":
                 buffer += sentence.text
                 pos += len(sentence)

            if sentence.tail is not None:
                buffer += sentence.tail
                pos += len(sentence.tail)

            #print(sentence)

        return buffer, posdict

root = xml.etree.ElementTree.fromstring("<dummy>"+w+"</dummy>")
sen, posdict = random_generate(root)
print(sen)
print(posdict)