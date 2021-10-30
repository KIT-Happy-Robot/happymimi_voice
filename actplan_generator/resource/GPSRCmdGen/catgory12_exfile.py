# !/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------
#author : fukuda_nao
#-------------------------------------------------------

import os
import random
import xml.etree.ElementTree as ET
import pexpect as pex
#import nltk
import sys
import time
#import subprocess as sub
DSPL_OPL=False
#question_file="/Category1.txt"

import random
import xml.etree.ElementTree as ET
common_data_path="GPSRCmdGen/Resources/"

tag_data=dict()
category_dict=dict()
gender_dict=dict()
room_dict=dict()

file="../cat1_dataset.txt"
for category in ET.parse(common_data_path+"/Objects.xml").getroot():
    for object in category:
        category_dict.setdefault(category.get("name"),{}).setdefault("object",[]).append(object.get("name"))
        category_dict[category.get("name")]["room"]=category.get("room")
        category_dict[category.get("name")]["location"]=category.get("defaultLocation")
tag_data["category"]=category_dict

for name in ET.parse(common_data_path+"/Names.xml").getroot():
    gender_dict.setdefault(name.get("gender"),[]).append(name.text)
tag_data["gender"]=gender_dict

for room in ET.parse(common_data_path+"/Locations.xml").getroot():
    for loc in room:
        room_dict.setdefault(room.get("name"),[]).append(loc.get("name"))
tag_data["room"]=room_dict
for ges in ET.parse(common_data_path+"/Gestures.xml").getroot():
    tag_data.setdefault("gestures",[]).append(ges.get("name"))


class DataMaker():
    def __init__(self,category="1"):
        self.category=category
    def cmdPlayer(self,cmd,cnt=10000,add=False):
        iv_str="Hit Enter to generate:"
        mode="a" if add else "w"
        gpsr_cmd=pex.spawn(cmd,encoding='utf-8')
        gpsr_cmd.logfile_read=open("cat"+self.category+"_ex_row.txt",mode)
        if gpsr_cmd.isalive():
            while cnt:
                index=gpsr_cmd.expect([iv_str,pex.EOF])
                if index==0:
                    gpsr_cmd.sendline(self.category)
                    cnt-=1
                elif index==1:
                    break
        gpsr_cmd.close()

    def main(self,add=True):
        self.cmdPlayer(cmd="make gpsr")
        self._GetNamesData_()
        question_ls=self.getQuestion()
        duplicate_confirmation=set()
        mode="w"
        if add:
            for s in open("cat"+self.category+"_dataset.txt","r"):
                duplicate_confirmation.add(s)

        with open("cat"+self.category+"_dataset.txt",mode) as f:
            for i in question_ls:
                i=self.ChangeNames(i)
                if i not in duplicate_confirmation:
                    duplicate_confirmation.add(i)
            for i in duplicate_confirmation:
                f.write(i)

    def allQuestionMaker(self):
        before_question=0
        self.main()
        cnt=0
        f=open("cat"+self.category+"_dataset.txt","r")
        question_len=sum([1 for _ in f])
        while before_question==question_len and cnt>3:
            if before_question==question_len:
                cnt+=1
            before_question=sum([1 for _ in f])
            f.close()
            self.main()
            f=open("cat"+self.category+"_dataset.txt","r")
            question_len=sum([1 for _ in f])
        f.close()


    def writeEXdata(self):
        #self.category=category
        question_ls=self.getQuestion()

        with open("cat"+self.category+"_ex.txt","w") as f:
            for i in question_ls:
                f.write(i)

    def getQuestion(self):
        with open("cat"+self.category+"_ex_row.txt","r") as f:
            str_flag=False
            line_cnt=0
            question_ls=[]
            for i in f:
                if str_flag:
                    line_cnt+=1
                    if line_cnt==4:
                        question_ls.append(i)

                    if line_cnt==5:
                        str_flag= not str_flag
                        if i.replace("\n",""):
                            question_ls[-1]=question_ls[-1].replace("\n"," ")+i
                if not DSPL_OPL and ("DSPL" in i or "OPL" in i) and len(question_ls)>0:
                    question_ls.pop(-1)


                if "Choosen category "+self.category in i:
                    str_flag= not str_flag
                    line_cnt=0
        return question_ls




    # xmlからオブジェクトとか部屋の名前を取得する
    # イニシャライザの中で呼び出される
    def _GetNamesData_(self):

        self.Obj_root = ET.parse(common_data_path+"Objects.xml").getroot()
        Nam_root = ET.parse(common_data_path+"Names.xml").getroot()
        self.Loc_root = ET.parse(common_data_path+ "Locations.xml").getroot()
        Ges_root = ET.parse(common_data_path+"Gestures.xml").getroot()

        self.CategoryData_word_list_nb = []
        self.ObjectData_word_list_nb = []
        self.NameData_word_list_nb = []
        self.RoomData_word_list_nb = []
        self.LocationData_word_list_nb = []
        #self.BeaconData_word_list_nb = []
        #self.PlacementData_word_list_nb = []
        self.GestureData_word_list_nb = []

        for ctg in self.Obj_root:
            self.CategoryData_word_list_nb.append(ctg.get("name"))
            for obj in ctg:
                self.ObjectData_word_list_nb.append(obj.get("name"))

        for nam in Nam_root:
            self.NameData_word_list_nb.append(nam.text)

        for rom in self.Loc_root:
            self.RoomData_word_list_nb.append(rom.get("name"))
            for loc in rom:
                self.LocationData_word_list_nb.append(loc.get("name"))
                #if loc.get("isBeacon"):
                    #self.BeaconData_word_list_nb.append(loc.get("name"))
                #if loc.get("isPlacement"):
                    #self.PlacementData_word_list_nb.append(loc.get("name"))

        for ges in Ges_root:
            self.GestureData_word_list_nb.append(ges.get("name"))

    def __del__(self):
        pass

    def ChangeNames(self, sentence):
        for i in self.GestureData_word_list_nb:
            sentence = sentence.replace(i, "{gesture}")
        for i in self.RoomData_word_list_nb:
            sentence = sentence.replace(i, "{room}")
        for i in self.LocationData_word_list_nb:
            sentence = sentence.replace(i, "{location}")
        for i in self.CategoryData_word_list_nb:
            sentence = sentence.replace(i, "{category}")
        for i in self.ObjectData_word_list_nb:
            sentence = sentence.replace(i, "{object}")
        for i in self.NameData_word_list_nb:
            sentence = sentence.replace(i, "{name}")
        return sentence

def writeExdata_by_origin():
    with open(file,"r") as f:
        question_ls=f.readlines()
    with open("cat1_ex.txt","w") as f:
        for question in question_ls:
            category=random.choice(list(tag_data["category"].keys()))
            object=random.choice(tag_data["category"][category]["object"])
            location=tag_data["category"][category]["location"]
            room=tag_data["category"][category]["room"]

            gesture=random.choice(tag_data["gestures"])
            gender=random.choice(list(tag_data["gender"].keys()))
            name=random.choice(tag_data["gender"][gender])

            question=question.replace("{gesture}",gesture).replace("{room}",room).replace("{location}",location).replace("{category}",category)\
                        .replace("{object}",object).replace("{name}",name)
            f.write(question)
        #d.main(category="2")


if __name__ == '__main__':
    if sys.argv[1]=="dataset1":
        d=DataMaker()
        d.allQuestionMaker()
    elif sys.argv[1]=="dataset2":
        d=DataMaker(category="2")
        d.allQuestionMaker()
    elif sys.argv[1]=="ex1":
        d=DataMaker()
        d.writeEXdata()
    elif sys.argv[1]=="ex2":
        d=DataMaker(category="2")
        d.writeEXdata()
    elif sys.argv[1]=="ex1_origin":
        writeExdata_by_origin()
    else:
        print("please set argv")
