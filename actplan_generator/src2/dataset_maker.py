
import MeCab
import pickle as pk

import re
import numpy as np

from sklearn import datasets


class DatasetMaker():
    def __init__(self,dataset_path="../resource",read_file="sequence_ex.txt",read_file2="sequence2.txt",
                input_out="input_str.txt",output_out="output_str.txt",input_id="input_id.txt",
                output_id="output_id.txt",lang="en",max_data=50000):
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
        self.dict_num[1]="<start>"
        self.dict_num[2]="<end>"
        self.dict_word["<PAD>"]=0
        self.dict_word["<start>"]=1
        self.dict_word["<end>"]=2

        self.word_number=2
        self.lang=lang
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
                    str4=re.sub(r"[.!?:;' ]", "",str3)
                    str4=re.sub(r"＊+","human",str4)
                    w.write(str4)


    def delethead(self,str_line,cnt):
        input_str=""
        output_str=""
        cnt = False
        if "input" in str_line:
            input_str=str_line.replace("input","")
            cnt = True

        else:
            output_str=str_line.replace("output","")
            cnt = False

        return (input_str,output_str,cnt)

    def sentenceSplit(self,sentence,inp):
        sentence_ls=[]
        delimiter_ls=[]
        del_ls = 0
        #listに変換
        str_ls=sentence.split()
        # print(str_ls)
        if inp:
            # delimiter_ls=[i for i,x in enumerate(str_ls) if "," in x or "and" in x]
            for i,x in enumerate(str_ls):
                if "," in x or "and" in x:
                    del_ls += 1
            delimiter_ls.append(del_ls)
            for i,num in enumerate(delimiter_ls):
                if i==0:
                    if "and" in str_ls[i]:
                        sentence_ls.append(str_ls[i])
                    else:
                        str_ls[i]=str_ls[i].replace(",","")
                        sentence_ls.append(str_ls[:i+1])
                else:
                    str_ls[i]=str_ls[i].replace(",","")
                    if len(delimiter_ls)-1 != i:
                        sentence_ls.append(str_ls[i+1:delimiter_ls[i+1]])
                    else:
                        sentence_ls.append(str_ls[i+1:])

        else:
            sub_ls=[]
            for i,word in enumerate(str_ls):
                sub_ls.append(word)
                if i%4==3:
                    sentence_ls.append(sub_ls)
                    sub_ls=[]

        # print(sentence_ls)
        return sentence_ls


    def segmentationwrite(self):
        input_txt=open(self.input_out,"w")
        output_txt=open(self.output_out,"w")
        cnt = False
        with open(self.read_file2,"r") as f:
            for str in f:
                # print("str:",str)
                input_str,output_str,cnt=self.delethead(str,cnt)
                # print(input_str)
                # print(output_str)
                # print(cnt)
                if cnt == True:
                    #sentence = self.sentenceSplit(input_str, True)
                    #input_txt.write(" ".join(sentence))
                    for sentence_in in self.sentenceSplit(input_str,True):
                        input_txt.write(" ".join(sentence_in))
                        #print(sentence)

                else:
                    #sentence = self.sentenceSplit(output_str, False)
                    #output_txt.write(" ".join(sentence))
                    for sentence_out in self.sentenceSplit(output_str,False):
                        output_txt.write(" ".join(sentence_out))
                        # print(sentence_out)

        input_txt.close()
        output_txt.close()



    def changer(self,file_name,write_name):
        with open(file_name,"r") as f:
            with open(write_name,"a") as w:
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

if __name__ == "__main__":
    datasetmaker = DatasetMaker()
    datasetmaker.all_run()
