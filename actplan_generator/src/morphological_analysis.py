#! /usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################
#ed 2021/9/17
#author fukuda nao
#comment: 形態素解析を使うものはここにまとめる. 英語に疎いため、有識者には更にいいコードを求む
##############################################################
import os.path
#import Levenshtein as lev
from nltk.tag.stanford import StanfordPOSTagger
import nltk
import numpy as np


file_path=os.path.expanduser('~/catkin_ws/src/happymimi_voice/config/dataset')

class MorphologicalAnalysis():
    def __init__(self,**kwargs):
        self.data_dict=kwargs
        #nltkのモデル読み込み
        self.pos_tag = StanfordPOSTagger(model_filename = file_path + "/stanford-postagger/models/english-bidirectional-distsim.tagger",
                                    path_to_jar = file_path + "/stanford-postagger/stanford-postagger.jar")



    def getActionplan(self,sentence):
        action_ls=[]
        target_ls=[]
        #action_sub=[]
        target_sub=[]
        target_cnt=0
        que_flag=False
        VB_flag=False
        if "speak_set" in self.data_dict:
            que_set=self.data_dict["speak_set"]
        que_set={"say","tell","answer"}
        pos_ls=self.pos_tag.tag(nltk.word_tokenize(sentence))  #品詞分解
        print(pos_ls)


        for word,tag in pos_ls:
            word=word.lower()
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

if __name__=="__main__":
    exclusion_VB={"leave"}
    action_set={"go":{"navigate","enter"}, "grasp":set(), "search":{"find","locate","look"}, "speak":{"tell","say","ask"},\
     "give":{"bring","take","deliver"}, "place":{"put"}, "approach":set(),"follow":set(),\
     "guide":{"escort","take","lead","accompany"},"answer":set(),"introduce":set()}
    m=MorphologicalAnalysis(speak_set=action_set["speak"],exclusion_VB=exclusion_VB)
    print(m.getActionplan("Follow William from the entrance to the corridor"))
