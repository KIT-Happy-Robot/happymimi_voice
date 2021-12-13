# -*- coding: utf-8 -*-

import MeCab
import pickle as pk

import re
import numpy as np

from sklearn import datasets


class DatasetMaker():
    def __init__(self,dataset_path="../data",read_file="sequence.txt",read_file2="sequence2.txt",
                input_out="input_str.txt",output_out="output_str.txt",input_id="input_id.txt",
                output_id="output_id.txt",lang="ja",max_data=50000):
        self.dataset_path=dataset_path
        self.read_file=dataset_path+"/"+read_file
        self.read_file2=dataset_path+"/"+read_file2
        self.input_out=dataset_path+"/"+input_out
        self.output_out=dataset_path+"/"+output_out
        self.input_id=dataset_path+"/"+input_id
        self.output_id=dataset_path+"/"+output_id
        self.dict_word={}
        self.dict_num={}
        self.dict_num[0]="<PAD>"
        self.dict_word["<PAD>"]=0
        self.dict_word["<start>"]=1
        self.dict_word["<end>"]=2
        self.dict_num[2]="<end>"
        self.dict_num[1]="<start>"
        self.word_number=2
        self.max_data=max_data
        with open(self.dataset_path+"/dataset_state.txt","w") as f:
            f.write("raw_data="+read_file+"\n")
            f.write("language="+lang)
            f.write("max_data="+str(max_data))

    def normalization(self):
        with open (self.read_file,"r") as f:
            with open(self.read_file2,"w") as w:
                for str in f:
                    #print(str)
                    str2=re.sub("\（.+?\）", "", str)
                    str3=re.sub("[A-Z]\d+","human",str2)
                    str4=re.sub(r"[,.!?:;' ]", "",str3)
                    str4=re.sub(r"＊+","human",str4)
                    w.write(str4)


    def delethead(self,str_line):
        input_str=""
        output_str=""
        if "input" in str_line:
            input_str=str_line.replace("input","")
        elif "output" in str_line:
            output_str=str_line.replace("output","")

        return (input_str,output_str)

    def segmentationwrite(self):
        wakati = MeCab.Tagger("-Owakati")
        input_txt=open(self.input_out,"w")
        output_txt=open(self.output_out,"w")
        with open(self.read_file2,"r") as f:
            for str in f:
                input_str,output_str=self.delethead(str)
                if input_str:
                    input_txt.write(wakati.parse(input_str))
                else:
                    output_txt.write(wakati.parse(output_str))
        input_txt.close()
        output_txt.close()


    def changer(self,file_name,write_name,):
        with open(file_name,"r") as f:
            with open(write_name,"w") as w:
                for i,str_line in enumerate(f):
                    if (i>=self.max_data):
                        break
                    id_str=[self.dict_word["<start>"]]
                    for word in str_line.replace("?"," ?").replace("."," .").replace("!"," !").split():
                        if word in self.dict_word:
                            id_str.append(self.dict_word[word])
                        else:
                            self.word_number=self.word_number+1
                            self.dict_word[word]=self.word_number
                            self.dict_num[self.word_number]=word
                            id_str.append(self.dict_word[word])
                    id_str.append(self.dict_word["<end>"])
                    w.write(' '.join(map(str,id_str))+"\n")
                    id_str.clear()

    def changeid(self):
        self.changer(self.input_out,self.input_id)
        self.changer(self.output_out,self.output_id)
        with open("../data/dict_word.pkl","wb") as p:
            pk.dump(self.dict_word,p)
            pk.dump(self.dict_num,p)



    def all_run(self):
        self.normalization()
        self.segmentationwrite()
        self.changeid()
