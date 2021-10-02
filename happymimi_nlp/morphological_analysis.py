# !/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################
#ed 2021/9/17
#author fukuda nao
#comment: 形態素解析を使うものはここにまとめる. 英語に疎いため、有識者には更にいいコードを求む
##############################################################
import os.path
import Levenshtein as lev
from nltk.tag.stanford import StanfordPOSTagger
import nltk
import numpy as np


file_path=os.path.expanduser('~/catkin_ws/src/happymimi_voice/dataset')

class MorphologicalAnalysis():
    def __init__(self):
        #nltkのモデル読み込み
        self.pos_tag = StanfordPOSTagger(model_filename = file_path + "/stanford-postagger/models/english-bidirectional-distsim.tagger",
                                    path_to_jar = file_path + "/stanford-postagger/stanford-postagger.jar")

    #汎用性を持たせるために形態素解析した結果を辞書型に(act_planではつかわない)
    def morphologicalAnalysis(self,sentence):
        dict_word={}
        pos_ls=self.pos_tag.tag(nltk.word_tokenize(sentence))
        for i,tag,word in enumerate(pos_ls):
            dict_word.setdefault(tag, []).append((word,i))
        print(dict_word)

        return dict_word


    #actplanで使う（GPSR）
    def getActionplan(self,sentence):
        action_ls=[]
        target_ls=[]
        action_sub=[]
        target_sub=[]
        NN_cnt=0
        #stemmer = nltk.stem.PorterStemmer() #単語を原型に直す（安定・一般）  バグった ex) cuntry → cuntri
        #stemmer = nltk.stem.LancasterStemmer()  #単語を原型に直す(アグレッシブ)
        clearList=lambda ls1,ls2 :[ls1.clear(),ls2.clear()] #subをクリアする無名関数
        joinList=lambda ls1,ls2 :ls1+list(reversed(ls2))         #順番を直したものを結合する

        IN_flag=0
        que_flag=False
        que_set={"say","tell","answer","Say","Tell","Answer"}
        tag_ls=["VB","IN","TO","NN"]
        exclusion_IN={"about","by","of"} #byは場所示すことあるんだよなぁ
        exclusion_tag={"DT"}
        pos_ls=self.pos_tag.tag(nltk.word_tokenize(sentence))  #品詞分解
        #print(pos_ls)
        for word,tag in pos_ls:
            if(tag in exclusion_tag):
                pass
            #word=stemmer.stem(word)#単語を原型に直す
            elif(word in que_set and tag_ls[0] in tag):   #tell say answerへの対処
                que_flag=True
                NN_cnt=0
                action_ls=joinList(action_ls,action_sub)
                target_ls=joinList(target_ls,target_sub)
                clearList(action_sub,target_sub)
                action_sub.append("speak")

            elif(word in ","):
                que_flag=False

            elif (que_flag): #tell sayのとき、以降の文をto前置詞が来るまで保存
                if(tag_ls[2] in tag):    #toの後は動詞と判断されるので
                    NN_cnt=0
                    action_sub.append("approach")
                elif(tag_ls[1] in tag and word not in exclusion_IN):
                    NN_cnt=0
                    action_sub.append("go")
                else:
                    NN_cnt+=1
                    if(NN_cnt>=2):
                        word=target_sub.pop()+" "+word #名詞を一文にまとめて格納し直す
                    target_sub.append(word)

            elif(tag_ls[0] in tag):   #動詞の抽出
                que_flag=False
                NN_cnt=0
                IN_flag=0
                IN_flag+=1
                action_ls=joinList(action_ls,action_sub)        #行動順番を直して結合（英語は後ろから訳す）
                target_ls=joinList(target_ls,target_sub)
                clearList(action_sub,target_sub)
                action_sub.append(word)

            elif((tag_ls[1] in tag or tag_ls[2] in tag) and IN_flag>=2 and word not in exclusion_IN):   #前置詞・toとフラグでgoアクションを追加するか判断
                NN_cnt=0
                action_sub.append("go")

            elif(tag_ls[2] in tag):
                NN_cnt=0
                action_sub.append("approach")

            elif(word=="it"):
                NN_cnt+=1
                IN_flag+=1
                target_sub.append(target_ls[-1]) #itは一つ前を指すと仮定


            elif(tag_ls[3] in tag or tag=="PRP"): #targetを抽出
                NN_cnt+=1
                IN_flag+=1
                if(NN_cnt>=2):
                    word=target_sub.pop()+" "+word #名詞を一文にまとめて格納し直す
                target_sub.append(word)

        action_ls=joinList(action_ls,action_sub)
        target_ls=joinList(target_ls,target_sub)
        clearList(action_sub,target_sub)

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
