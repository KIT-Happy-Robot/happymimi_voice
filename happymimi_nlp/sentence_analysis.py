#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Levenshtein as lev
import fuzzy
#from nltk.tag.stanford import StanfordPOSTagger
import nltk
import numpy as np
import copy
file_path="../config"
#import spacy

# 引数 認識文　変更しない正しい文split 結果に書き換えていく正しい文split タグの要素番号　対応タグのリスト　タグ名　
def wordVerification(recog_sentence,sentence_ls,result_question,tag_data,xml_data,tag_name,):
    dmeta = fuzzy.DMetaphone()
    get_tag=[]
    current_quetion=copy.deepcopy(sentence_ls)
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
                        list1.append(a)

                for k in recog_sentence.replace(',', ' ,').split():
                    b = dmeta(k)[0]
                    if b!=None:
                        list2.append(b)

                #print(' '.join(list1) + "\t\t:" + ' '.join(list2))
                distance.append(lev.ratio(' '.join(list1), ' '.join(list2))*1.00)
                #print(str(distance[-1]) + "\t\t:" +' '.join(cvt_word_list_cnb))
            tag_data.append(xml_data[distance.index(max(distance))])
            result_question[num] = tag_data[-1]
            get_tag.append(tag_data[-1])
            #print(distance)
    except IndexError:
        print("IndexError")
        pass
    except TypeError:
        print("TypeError")
        pass

    return get_tag

def levSearch(word:str,com_ls:list,default_v=0.6,fuz=False,get_value=False)->int:
    current_str=-1
    error_f=False
    if fuz:
        try:
            dmeta = fuzzy.DMetaphone()
            word=dmeta(word)[0]
            for i,string in enumerate(com_ls):
                str1=dmeta(string)[0]

                value=lev.ratio(word,str1)
                #print(word,value)
                #value=lev.distance(word, str)/(max(len(word), len(str)) *1.00)
                if (default_v<value):
                    default_v=value
                    current_str=i
                    #print(str)
            #print(default_v)
        except IndexError:
            print("IndexError")
            error_f=True
        except TypeError:
            print("TypeError")
            error_f=True
    if(fuz==False or error_f):
        try:
            for i,string in enumerate(com_ls):
                value=lev.ratio(word,string)
                #value=lev.distance(word, string)/(max(len(word), len(string)) *1.00)
                if (default_v<value):
                    default_v=value
                    current_str=i
        except TypeError:
            if get_value:
                return current_str,default_v
            return current_str
        #print(default_v)
    if get_value:
        return current_str,default_v
    return current_str


def branchMake(token,dep=0):
    print(dep * '_' + token.text)
    for child in token.children:
        branchMake(child, dep + 1)

# docからセンテンスを取り出しルート要素から木構造を出力する

class MorphologicalAnalysis():
    def __init__(self,**kwargs):
        self.data_dict=kwargs
        #nltkのモデル読み込み
        '''
        self.pos_tag = StanfordPOSTagger(model_filename = file_path + "/dataset/stanford-postagger/models/english-bidirectional-distsim.tagger",
                                    path_to_jar = file_path + "/dataset/stanford-postagger/stanford-postagger.jar")

        '''
        self.pos_tag= spacy.load("en_core_web_trf")

    #汎用性を持たせるために形態素解析した結果を辞書型に(act_planではつかわない)
    def morphologicalAnalysis(self,sentence):
        pos_ls=self.pos_tag(sentence)
        return pos_ls

    def actionGet(self,sentence):
        action_ls=[]
        target_ls=[]
        #action_sub=[]
        target_sub=[]
        target_cnt=0
        que_flag=False
        VB_flag=False
        if "speak_set" in self.data_dict:
            que_set=self.data_dict["speak_set"]
        else:
            que_set={"say","tell","answer"}
        #pos_ls=self.pos_tag.tag(nltk.word_tokenize(sentence))  #品詞分解
        pos_ls=self.pos_tag(sentence)


        for pos in pos_ls:
            word = pos.text
            tag=pos.tag_
            children=list(pos.children)
            #word=stemmer.stem(word)#単語を原型に直す
            if(word in que_set):   #tell say answerへの対処
                VB_flag=True
                action_ls.append("speak")
                if target_cnt>0:
                    target_ls.append(target_sub)
                    target_sub=[]
                    target_cnt=0

            elif(word in "," or word in "." or tag in "CC"):
                VB_flag=False
                continue

            elif "exclusion_VB" in self.data_dict and word in self.data_dict["exclusion_VB"]:
                target_sub.append((word,tag))

            elif "VB" in tag and "VBP"!=tag and "VBZ"!=tag:   #動詞の抽出
                VB_flag=True
                action_ls.append(word)
                if target_cnt>0:
                    target_ls.append(target_sub)
                    target_sub=[]
                    target_cnt=0

            elif VB_flag: #targetを抽出
                target_cnt+=1
                target_sub.append((word,tag))

        if target_cnt>0:
            target_ls.append(target_sub)

        return action_ls,target_ls




    def infoTag(self):
        print(  "CC	Coordinating conjunction 調整接続詞",
                "CD	Cardinal number	基数",
                "DT	Determiner	限定詞",
                "EX	Existential there	存在を表す there",
                "FW	Foreign word	外国語",
                "IN	Preposition or subordinating conjunction	前置詞または従属接続詞",
                "JJ	Adjective	形容詞",
                "JJR	Adjective, comparative	形容詞 (比較級)",
                "JJS	Adjective, superlative	形容詞 (最上級)",
                "LS	List item marker",
                "MD	Modal	法",
                "NN	Noun, singular or mass	名詞",
                "NNS  Noun,  plural 名詞 (複数形)",
                "NNP	Proper noun, singular	固有名詞",
                "NNPS	Proper noun, plural	固有名詞 (複数形)",
                "PDT	Predeterminer	前限定辞",
                "POS	Possessive ending	所有格の終わり",
                "PRP	Personal pronoun	人称代名詞 (PP)",
                "PRP$	Possessive pronoun	所有代名詞 (PP$)",
                "RB	Adverb	副詞",
                "RBR	Adverb, comparative	副詞 (比較級)",
                "RBS	Adverb, superlative	副詞 (最上級)",
                "RP	Particle	不変化詞",
                "SYM	Symbol	記号",
                "TO	to	前置詞 to",
                "UH	Interjection	感嘆詞",
                "VB	Verb, base form	動詞 (原形)",
                "VBD	Verb, past tense	動詞 (過去形)",
                "VBG	Verb, gerund or present participle	動詞 (動名詞または現在分詞)",
                "VBN	Verb, past participle	動詞 (過去分詞)",
                "VBP	Verb, non-3rd person singular present	動詞 (三人称単数以外の現在形)",
                "VBZ	Verb, 3rd person singular present	動詞 (三人称単数の現在形)",
                "WDT	Wh-determiner	Wh 限定詞",
                "WP	Wh-pronoun	Wh 代名詞",
                "WP$	Possessive wh-pronoun	所有 Wh 代名詞",
                "WRB	Wh-adverb	Wh 副詞",end="\n")

if __name__=='__main__':
    i=input()
    pos_tag= spacy.load("en_core_web_trf")
    #for sent in pos_tag(i).sents:
        #branchMake(sent.root)
    #    print(sent)
    for j in pos_tag(i):
        print(j.text,list(j.children))
