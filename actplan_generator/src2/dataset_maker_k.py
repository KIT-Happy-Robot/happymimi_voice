
import MeCab
import pickle as pk

import re
import numpy as np
import io
from sklearn import datasets

import itertools

class DatasetMaker():
    def __init__(self,dataset_path="../resource/src1_2",
                 read_file="sequence_ex.txt",
                 read_file2="sequence2.txt",
                 input_out="input_str_k.txt",output_out="output_str_k.txt",
                 input_id="input_id_k.txt",output_id="output_id_k.txt",
                 lang="en",max_data=70000):
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
            f.write("language="+lang+"\n")
            f.write("max_data="+str(max_data))

    # def normalization(self):
        # with open (self.read_file,"r") as f:
            # with open(self.read_file2,"w") as w:
                # for str in f:
                    #print(str)
                    # str2=re.sub("\（.+?\）", "", str)
                    # str3=re.sub("[A-Z]\d+","human",str2)
                    # str4=re.sub(r"[.!?:;' ]", "",str3)
                    # str4=re.sub(r"＊+","human",str4)
                    # w.write(str4)

    def prepare_sentence(self):
        with open(self.read_file, "r") as f:
            with open(self.read_file2, "w") as w:
                for str in f:
                    sentence = str.lower().strip()
                    sentence = re.sub(r"([?.!,¿])", r" \1 ", sentence)
                    sentence = re.sub(r'[" "]+', " ", sentence)
                    sentence = re.sub(r"[^a-zA-Z?.!,¿]+", " ", sentence)
                    sentence = sentence.rstrip(" .").strip()
                    # sentence = '<start>' + sentence + '<end>\n'
                    w.write(sentence+"\n")


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
        #listに変換
        str_ls=sentence.split()
        if inp:
            for i,x in enumerate(str_ls):
                if "," in x or "and" in x:
                    delimiter_ls.append(i)

            if len(delimiter_ls) == 1:
                sentence_ls.append(str_ls[:delimiter_ls[0]])
                sentence_ls.append(str_ls[delimiter_ls[0]+1:])

            elif len(delimiter_ls) == 0:
                return str_ls, 0

            else:
                sentence_ls.append(str_ls[:delimiter_ls[0]])
                sentence_ls.append(str_ls[delimiter_ls[0]+1:delimiter_ls[1]])
                sentence_ls.append(str_ls[delimiter_ls[1]+2:])

        else:
            sub_ls=[]
            for i,word in enumerate(str_ls):
                sub_ls.append(word)
                if i%4==3:
                    sentence_ls.append(sub_ls)
                    sub_ls=[]

        return sentence_ls, 1


    def segmentationwrite(self):
        input_txt=open(self.input_out,"w")
        output_txt=open(self.output_out,"w")
        cnt = False
        sentence_in = []
        sentence_out = []
        with open(self.read_file2,"r") as f:
            for str_sen in f:
                input_str,output_str,cnt=self.delethead(str_sen,cnt)
                if cnt == True:
                    a,count = self.sentenceSplit(input_str,True)
                    if count == 0:
                        input_txt.write(" ".join(map(str,a))+ '\n')

                    else:
                        lst_a = list(itertools.chain.from_iterable(a))
                        input_txt.write(" ".join(map(str, lst_a))+ '\n')
                else:
                    b, count= self.sentenceSplit(output_str, False)
                    lst_b = list(itertools.chain.from_iterable(b))
                    output_txt.write(" ".join(map(str, lst_b))+ '\n')

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
        #self.prepare_sentence()
        #self.segmentationwrite()
        self.changeid()

if __name__ == "__main__":
    datasetmaker = DatasetMaker()
    datasetmaker.all_run()
