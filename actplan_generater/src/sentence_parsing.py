#! /usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################
#ed 2021/10/18
#writen by python3.8
#author fukuda nao and onisi
#comment: 多重辞書にデータをまとめたため複雑になってしまった,はじめ形態素解析だけでなんとかしようとしてたので複雑になってしまっている,
#本プログラムでは形態素解析する必要はなかったが修正が面倒なのでこのままにしてある
#類似度計算を使って動詞を探すのもあり
#python3.8以降でしか動かない
##############################################################


import os.path
import Levenshtein as lev
import xml.etree.ElementTree as ET
#import difflib as dif
#happymimi_voiceにもある
#import morphological_analysis as morph
#import word2vec_analysis as w2v
import datetime
import nltk
import sys
import roslib.packages
import fuzzy
import copy

file_path=roslib.packages.get_pkg_dir("actplan_generator")+"/resource"
#get
question_file="/cat1_dataset.txt"


common_data_path="/GPSRCmdGen/CommonFiles"

exclusion_VB={"leave"}
#できない単語をリストアップ
everyone_ls=["everyone"]
everyone_ls.extend(["all the "+i for i in ["people", "men", "women" , "guests" , "elders" , "children"]])
another_object=["bag" , "baggage" , "valise" , "suitcase" , "trolley"]
another_location=["taxi" , "cab" , "uber"]
cant_ls=another_object+another_location+everyone_ls
person_set={"woman","man","person","boy","girl"}

add_location={"door":{"front","back","main", "rear","entrance","door"}}
#add follow answer
command_ls=["go", "grasp", "find", "speak", "give", "place", "approach","follow","answer"]
#origin_com=["guide","introduce"]

action_set={"go":{"navigate","enter"}, "grasp":set(), "find":{"search","locate","look"}, "speak":{"tell","say","ask"},\
 "give":{"bring","take","deliver"}, "place":{"put"}, "approach":set(),"follow":set(),\
 "guide":{"escort","take","lead","accompany"},"answer":set(),"introduce":set(),"grasp":{"take","pick","get"}}

[action_set["give"].add(i) for i in ["distribute","provide","arrange","serve"]]
[action_set["approach"].add(i) for i in ["contact","face","find","greet","meet"]]
#skip:None 一つ前のtargetがnoneのときスキップ
action_dict={"give":["go","grasp","approach","give"],"guide":["approach","speak:please follow me","go"],\
"introduce":["go","skip:None","approach","speak:The person in the {BeforeRoom} is {BeforeName}"],"follow":["speak:I will follow you","follow"],"speak":["go","approach","speak"],\
"find":["go","skip:None","find"],"place":["go","place"],"grasp":["go","grasp"],"approach":["go","skip:None","approach"],"answer":["go","skip:None","approach","answer"]}



class SentenceParsing():
    def __init__(self,start_place="living room",category3=False):
        self.question_ls=[i for i in open(file_path+question_file,"r")]
        self.tag_data={"category":{},"gender":{},"room":{}}
        #self.start_place=start_place
        self.category3=category3
        #self.morph_str=morph.MorphologicalAnalysis(speak_set=action_set["speak"],exclusion_VB=exclusion_VB)
        self.dataFormating()

    #事前データの読み込み・整形
    def dataFormating(self):
        #発表されたデータ
        category_dict={}
        gender_dict={}
        room_dict={}
        for category in ET.parse(file_path+common_data_path+"/Objects.xml").getroot():
            for object in category:
                category_dict.setdefault(category.get("name"),{}).setdefault("object",[]).append(object.get("name"))
                category_dict[category.get("name")]["room"]=category.get("room")
                category_dict[category.get("name")]["location"]=category.get("defaultLocation")
        self.tag_data["category"]=category_dict

        for name in ET.parse(file_path+common_data_path+"/Names.xml").getroot():
            gender_dict.setdefault(name.get("gender"),[]).append(name.text)
        self.tag_data["gender"]=gender_dict

        for room in ET.parse(file_path+common_data_path+"/Locations.xml").getroot():
            for loc in room:
                room_dict.setdefault(room.get("name"),[]).append(loc.get("name"))
        self.tag_data["room"]=room_dict
        for ges in ET.parse(file_path+common_data_path+"/Gestures.xml").getroot():
            self.tag_data.setdefault("gestures",[]).append(ges.get("name"))
        #print(self.tag_data)
        #question_lsでレーベンシュタイン距離を取れるよう整形

        #for i in range(len(self.question_ls)):
        #    self.question_ls[i]=self.question_ls[i].replace("{object}","{O}").replace("{location}","{L}").replace("{room}","{R}").replace("{name}","{N}").replace("{category}","{C}").replace("{gesture}","{G}")


    def levSearch(self,word,com_ls,default_v=0.600000):
        current_str=-1

        for i,str in enumerate(com_ls):
            value=lev.ratio(word,str)
            #value=lev.distance(word, str)/(max(len(word), len(str)) *1.00)
            if (default_v<value):
                default_v=value
                current_str=i
        #print(default_v)
        return current_str

    def wordVerification(self,tag_data,xml_data,tag_name):
        dmeta = fuzzy.DMetaphone()
        current_quetion=copy.deepcopy(self.current_quetion)
        try:
            while(isinstance(tag_data[0], int)):
                num = tag_data.pop(0)
                distance = []
                for i in xml_data:
                    current_quetion[num] = i
                    list1 = []
                    list2 = []
                    for j in current_quetion:
                        a = dmeta(j)[0]
                        if a!=None:
                            list1.append(a.decode())

                    for k in self.recog_sentence.replace(',', ' ,').split():
                        b = dmeta(k)[0]
                        if b!=None:
                            list2.append(b.decode())

                    #print(' '.join(list1) + "\t\t:" + ' '.join(list2))
                    distance.append(lev.ratio(' '.join(list1), ' '.join(list2))*1.00)
                    #print(str(distance[-1]) + "\t\t:" +' '.join(cvt_word_list_cnb))
                tag_data.append(xml_data[distance.index(max(distance))])
                self.word_ls.append(tag_data[-1])
                self.tag_ls.append(tag_name)
                self.result_question[num] = tag_data[-1]
                #print(distance)
        except IndexError:
            print("IndexError")
            pass
        except TypeError:
            print("TypeError")
            pass

    def questionFormating(self,sentence):
        self.recog_sentence=sentence
        self.tag_ls=[]
        self.word_ls=[]
        str=self.nameChange(sentence)
        current_quetion=self.levSearch(str,self.question_ls,default_v=0.4)
        if(current_quetion==-1):
            quetion_str=sentence
            print("unknown sentence")
            return "ERROR"
        else:
            self.current_quetion=self.question_ls[current_quetion].lower().replace(',', ' ,').split()
            self.result_question = self.question_ls[current_quetion].lower().replace(',', ' ,').split()
            category = [i for i, x in enumerate(self.current_quetion) if x == "{category}"]
            object = [i for i, x in enumerate(self.current_quetion) if x == "{object}"]
            name = [i for i, x in enumerate(self.current_quetion) if x == "{name}"]
            room = [i for i, x in enumerate(self.current_quetion) if x == "{room}"]
            location = [i for i, x in enumerate(self.current_quetion) if x == "{location}"]
            #print([i for k,v in self.tag_data["gender"].items() for i in v])
            if category:
                self.wordVerification(category,list(self.tag_data["category"].keys()),"{category}")
            if object:
                self.wordVerification(object,[i for k,v in self.tag_data["category"].items() for i in v["object"]],"{object}")
            if name:
                self.wordVerification(name,[i for k,v in self.tag_data["gender"].items() for i in v],"{name}")
            if room:
                self.wordVerification(room,list(self.tag_data["room"].keys()),"{room}")
            if location:
                self.wordVerification(location,[i for k,v in self.tag_data["room"].items() for i in v],"{location}")

        return " ".join(self.result_question)



    def makeAnswer(self,sentence)->str:
        dt_now=datetime.datetime.now()
        week_ls=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday','Monday']
        month_ls=[None, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                'September', 'October', 'November', 'December']
        answer_dict={"country":"Japan", "affiliation":"kanazawa institute of technology",
                    "day is tomorrow":week_ls[dt_now.weekday()+1], "day is today":week_ls[dt_now.weekday()],
                    "time":"It’s "+str(dt_now.hour)+" "+str(dt_now.minute), "day of the week":week_ls[dt_now.weekday()] ,
                    "day of the month":"Today is "+str(dt_now.day), "something about yourself":"my name is mimi",
                    "joke":"Can a kangaroo jump higher than a house? of course, a house doesn't jump at all.",
                     "team 's name":"happy mimi", "question":"please question for me","how many":"1","to leave":"please leave here"}

        for k,v in answer_dict.items():
            if k in sentence:
                return v

    #category1,2 no 3 （オブジェクトの場所優先） 複数のtarget(ex:grasp bottle and food)はでなさそうなので考慮してない
    def targetGet(self,action,target_ls,same_flag=False) -> list:
        category,object,person,gender,location,room="","","","","",""
        before_object,before_category,before_person=self.before_data.get("object"),self.before_data.get("category"),self.before_data.get("person")
        before_location,before_room=self.before_data.get("location"), self.before_data.get("room")
        #代名詞等を置換する
        indexGet=lambda x:[i for i,w in enumerate(target_ls) if w==x]
        it_index=indexGet("it")
        #there_index=indexGet("there")
        himher_index=indexGet("him") if indexGet("him") else indexGet("her")
        if it_index:
            if before_object:
                for i in it_index:
                    target_ls[i]=before_object
            elif before_category:
                for i in it_index:
                    target_ls[i]=before_category
            elif before_person:
                for i in it_index:
                    target_ls[i]=before_person
        '''
        if there_index:
            for i in there_index:
                target_ls[i]=self.before_data.get("location")
        '''

        if himher_index:
            for i in himher_index:
                target_ls[i]=self.before_data.get("person")

        if "me" in target_ls:
            self.approach_flag=True
            person="operator"
        if person_set & set(target_ls):
            person="person"
        #print(action,target_ls)
        sentence=" ".join(target_ls)

        for i,(tag,word) in enumerate(zip(self.tag_ls,self.word_ls)):
            if word in sentence:
                if tag=="{object}":
                    object=word
                elif tag=="{category}":
                    category=word
                elif tag=="{name}":
                    person=word
                elif tag=="{location}":
                    location=word
                elif tag=="{room}":
                    room=word

        for k,v in add_location.items():
            for d in v:
                if d in target_ls:
                    location=k
                    break
            if k in target_ls:
                location=k
                break

        ob_loc=[v["location"] for k,v in self.tag_data["category"].items() if object in v["object"]]
        location=ob_loc[0] if ob_loc else location
        if category:
            location=self.tag_data["category"][category]["location"]

        if location:
            if room_ls:=[k for k,v in self.tag_data["room"].items() if location in v]:
                room=room_ls[0]




        #beforeの更新
        if not same_flag:
            self.before_data["category"]=category
            self.before_data["object"]=object
            self.before_data["person"]=person
            self.before_data["location"]=location
            self.before_data["room"]=room

        if action=="grasp":
            if object:
                self.grasp_flag=True
                return action,object
            elif category:
                self.grasp_flag=True
                return action,category
        elif action=="give":
            if object:
                self.grasp_flag=False
                return action,object
            elif category:
                self.grasp_flag=False
                return action,category

        if action=="go" and location:
            self.approach_flag=False
            return action,location
        elif action=="go" and room:
            self.approach_flag=False
            return action,room
        elif (action=="approach" or action=="find" or action=="follow") and person:
            if person=="operator":
                return "go",person
            self.approach_flag=True
            return action,person
        elif (action=="place" or action=="find" ) and object:
            self.approach_flag=False
            return action,object
        elif (action=="place" or action=="find" ) and category:
            self.approach_flag=False
            return action,category
        elif action=="speak" and self.approach_flag:
            return action,self.makeAnswer(sentence)
        elif action=="answer" and self.approach_flag:
            return action,"please question for me"
        elif "speak:" in action and self.approach_flag:
            if not before_person:
                before_person=person
            if not before_room:
                before_room=room
            for k,v in self.tag_data["gender"].items():
                if before_person in v:
                    gender=k
                break
            if gender=="Male":
                Genitive="his"
            elif gender=="Female":
                Genitive="her"
            else:
                Genitive=""
            action=action.replace("speak:","").replace("{BeforGenitive}",Genitive).replace("{BeforeName}",before_person).replace("{BeforeRoom}",before_room)
            return "speak",action
        else:
            #print(action,target_ls)
            #print(self.tag_ls,self.word_ls)
            return None,None


    #カテゴリ3は未対応
    def makePlan(self,quetion_str):
        action_ls,targets_ls=self.splitTarget(nltk.word_tokenize(quetion_str))
        #拡張性を高めるためにあえてif文を細かく書く
        def flagAction(flag_action:list,action_n:str,targets:list):
            index=action_dict[flag_action].index(action_n)
            for v in action_dict[action][index+1:-1]:
                if "skip:" in v:
                    if "None" in v and target_sub[-1]==None:
                        action_sub.pop(-1)
                        target_sub.pop(-1)

                    continue
                a,t=self.targetGet(v,targets,True)
                action_sub.append(a)
                target_sub.append(t)


        self.before_data={}
        self.grasp_flag=False
        grasp_action=[k for k,v in action_dict.items() if "grasp" in v]
        self.approach_flag=False
        approach_action=[k for k,v in action_dict.items() if "approach" in v]

        action_sub,target_sub=[],[]

        for i,(action,targets) in enumerate(zip(action_ls,targets_ls)):
            #前回の人と次のターゲットが違うときapproach_flag=False
            if self.approach_flag:
                for i,(tag,word) in enumerate(zip(self.tag_ls,self.word_ls)):
                    if word in targets and tag=="{name}" and self.before_data.get("person")!=word:
                        self.approach_flag=False
            elif action=="speak" and "me" in targets:
                self.approach_flag=True
            if action_dict.get(action):
                if action in grasp_action and self.grasp_flag:
                    flagAction(action,"grasp",targets)

                elif action in approach_action and self.approach_flag:
                    flagAction(action,"approach",targets)

                else:
                    for p in action_dict[action][:-1]:
                        if "skip:" in p:
                            if "None" in p and target_sub[-1]==None:
                                action_sub.pop(-1)
                                target_sub.pop(-1)
                            continue
                        a,t=self.targetGet(p,targets,True)
                        action_sub.append(a)
                        target_sub.append(t)
                a,t=self.targetGet(action_dict[action][-1],targets)
                action_sub.append(a)
                target_sub.append(t)

            elif action in command_ls:
                a,t=self.targetGet(action,targets)
                action_sub.append(a)
                target_sub.append(t)
            else:
                t=None
                action_sub.append(None)
                target_sub.append(None)

        if None in action_sub or None in target_sub:
            print("Failed to make a plan")
            print(action_sub,target_sub)
            return None,None
        return action_sub,target_sub

    def nameChange(self,sentence):
        for k,v in self.tag_data["category"].items():
            sentence = sentence.replace(k, "{category}")
            for i in v["object"]:
                sentence = sentence.replace(i, "{object}")
        for v in self.tag_data["gender"].values():
            for i in v:
                sentence = sentence.replace(i, "{name}")
        for k,v in self.tag_data["room"].items():
            sentence = sentence.replace(k, "{room}")
            for i in v:
                sentence = sentence.replace(i, "{location}")
        for i in self.tag_data["gestures"]:
             sentence = sentence.replace(i, "{gesture}")
        return sentence

    def availabilityJudgement(self,sentence):
        for i in cant_ls:
            if i in sentence:
                print("warnning word:"+i)
                return False
        return True

    def splitTarget(self,words:list):
        action_index=[]
        skip_set={",",".","and"}
        action_ls,target_ls=[],[]
        target_sub=[]
        target_cnt=0
        start_flag=False
        for i,word in enumerate(words):
            action_flag=False
            if word in skip_set:
                continue
            for k,v in action_set.items():
                if k==word.lower() or word.lower() in v:
                    action_flag=True
                    start_flag=True
                    action_ls.append(k)
                    if target_cnt>0:
                        target_ls.append(target_sub)
                        target_sub=[]
                        target_cnt=0
                    break
            if start_flag and not action_flag:
                target_sub.append(word)
                target_cnt+=1

        target_ls.append(target_sub)
        return action_ls,target_ls





def debuger(category="1"):
    str_pars=SentenceParsing()
    sys.stdout = open('../resource/fail.log', 'w')
    ex_path="../resource/cat"+category+"_ex.txt"
    success_question=open("../resource/success_question.txt","w")
    #fail_question=open("../resource/fail_question.txt","a")

    for question in open(ex_path,"r"):
        current_quetion=str_pars.questionFormating(question)
        if current_quetion=="ERROR":
            print("not found sentence : ",question)
            continue
        elif not str_pars.availabilityJudgement(current_quetion):
            print(question)
            continue
        a,t=str_pars.makePlan(current_quetion)


        if a==None or t==None:
            print(question)

        else:
            #print(question)
            #print(a,t)
            success_question.write(question+" "+",".join(a)+"   "+",".join(t)+"\n"+"\n")

if __name__=="__main__":
    #NAaction()
    debuger()
    #s=SentenceParsing()
    #s.main("Look for the fruits in the bedroom")
