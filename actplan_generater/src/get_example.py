# !/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------
#author : fukuda_nao
#-------------------------------------------------------
import random
import xml.etree.ElementTree as ET


tag_data=dict()
category_dict=dict()
gender_dict=dict()
room_dict=dict()

file="../resource/cat1_dataset.txt"
common_data_path="../resource/GPSRCmdGen/CommonFiles"
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


def getExample():
    with open(file,"r") as f:
        question_ls=f.readlines()

    while 1:
        question=random.choice(question_ls)
        category=random.choice(list(tag_data["category"].keys()))
        object=random.choice(tag_data["category"][category]["object"])
        location=tag_data["category"][category]["location"]
        room=tag_data["category"][category]["room"]

        gesture=random.choice(tag_data["gestures"])
        gender=random.choice(list(tag_data["gender"].keys()))
        name=random.choice(tag_data["gender"][gender])

        question=question.replace("{gesture}",gesture).replace("{room}",room).replace("{location}",location).replace("{category}",category)\
                    .replace("{object}",object).replace("{name}",name)

        print(question)
        s=input("n:next   f:finish :")
        if "f" in s:
            break

if __name__=="__main__":
    getExample()
