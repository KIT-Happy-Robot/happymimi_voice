#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
from os import path
#発話
#from gcp_texttospeech.srv import TTS
from happymimi_msgs.srv import StrTrg
#音声認識
from happymimi_voice_msgs.srv import SpeechToText
#word2vec(どのくらい似てるか)
import gensim.downloader as api
import sys
from happymimi_voice_msgs.srv import GgiLearning
from happymimi_voice_msgs.srv import GgiLearningResponse
from nltk.tag.stanford import StanfordPOSTagger
import rospy
import random

file_path=path.expanduser('~/catkin_ws/src/happymimi_voice/config')
minimum_value=0.5 #コサイン類似度の最低値
#ベクトル読み込み
print("data loading...")
word_vectors = api.load("glove-twitter-200")
#nltkのモデルを読み込む
pos_tag = StanfordPOSTagger(model_filename = file_path + "/stanford-postagger/models/english-bidirectional-distsim.tagger",
                            path_to_jar = file_path + "/stanford-postagger/stanford-postagger.jar")

class GgiTest():
    def __init__(self):
        #ベクトル読み込み
        print('Wahing for tts and stt_server')
        rospy.wait_for_service('/tts')
        rospy.wait_for_service('/stt_server')
        print('test_phase is ready')
        self.stt=rospy.ServiceProxy('/stt_server',SpeechToText)
        self.tts=rospy.ServiceProxy('/tts', StrTrg)
        self.server=rospy.Service('/test_phase',GgiLearning,self.main)


    def main(self,req):
        switch_num=0
        print("start test_phase")
        #登録したファイルを読み込む
        if not path.isfile(file_path+'/object_file.pkl'):
            print('not found object file')
            sys.exit()

        else:
            with open(file_path+'/object_file.pkl','rb') as f:
                self.dict=pickle.load(f)

        #オペレーターの指示を認識
        while 1:

            name=[]
            name_feature=[]
            place=[]
            place_feature=[]
            #音声認識
            string=self.stt(short_str=False)

            shut='shut down'
            #shut downを認識したら終了
            if  shut in string.result_str:
                self.tts("shut down")
                break

            else:
                i=0
                #形態素解析
                pos = pos_tag.tag(string.result_str.split())
                #場所とオブジェクトそれぞれの特徴と名前をいつにまとめる
                while i<len(pos):
                    #前置詞かつofではなかったら場所のリストに追加
                    if pos[i][1] =='IN' and pos[i][0]!='of':
                        for j in range(i,len(pos)):
                            if 'NN' in pos[j][1]:
                                place.append(pos[j][0])
                                if j!=(len(pos)-1):
                                    if not 'NN' in pos[j+1][1]:
                                        break
                            elif pos[j][1]=='JJ':
                                place_feature.append(pos[j][0])
                        i=j+1
                        continue
                    #前置詞かつofだったらもののリストに追加
                    elif pos[i][1] =='IN' and pos[i][0]=='of':

                        for k in range(i,len(pos)):
                            if 'NN' in pos[k][1]:
                                name.append(pos[k][0])
                                if k!=(len(pos)-1):
                                    if not 'NN' in pos[k+1][1]:
                                        break
                            elif pos[k][1]=='JJ':
                                name_feature.append(pos[k][0])
                        i=k+1
                        continue
                    #ものの名前のリストに追加
                    elif 'NN' in pos[i][1]:
                        name.append(pos[i][0])
                    #ものの特徴のリストに追加
                    elif pos[i][1]=='JJ':
                        name_feature.append(pos[i][0])
                    i+=1
                print(name)
                print(place)
                print(name_feature)
                print(place_feature)


                #ggi_learingで学習した内容から探索
                search_class=SearchObject(self.stt,self.tts,self.dict)
                str=search_class.main(name,name_feature,place,place_feature,switch_num)
                if str=='no':
                    self.tts('one more time')
                    continue
                elif str:
                    return GgiLearningResponse(location_name=str)
                else:
                    self.tts("I don't know " )
                    self.tts('one more time')
                    switch_num+=1




class SearchObject():

    def __init__(self,stt_server,tts_server,dict_data:dict):
        self.stt_server=stt_server
        self.tts_server=tts_server
        self.dict=dict_data
        self.long=len(dict_data['place_name'])


    def main(self,name:list,name_feature:list,place:list,place_feature:list,switch_num:int):
        #登録した情報分だけそれぞれ確認する
        for i in range(self.long):
            #ものの名前と場所の名前の一致を確認
            branch = self.matchedSearch('object_name','place_name',name,place,i)
            if branch:
                return branch

        for i in range(self.long):
            #場所の名前と特徴が一致している
            branch=self.matchedSearch('place_name','place_feature',place,place_feature,i)
            if branch:
                return branch

        #類似度計算
        name_similarity=self.matchedWord2vec("object_name",name)# =>int or bool
        place_similarty=self.matchedWord2vec("place_name",place)
        #同じ場所を示していたら
        if name_similarity==place_similarty and name_similarity != False:
            return self.wordJoin(name_similarity)

        for i in range(self.long):
            #ものの名前と特徴の一致
            branch = self.matchedSearch('object_name','object_feature',name,name_feature,i)
            if branch:
                return branch

        #最終オブジェクト名または場所名で判断
        if switch_num%2==0 :
            if name_similarity != False:
                return self.wordJoin(name_similarity)
            elif place_similarty != False:
                return self.wordJoin(place_similarty)
            else:
                return self.wordJoin(random.randrange(self.long))

        elif switch_num%2==1:
            if place_similarty != False:
                return self.wordJoin(place_similarty)
            elif name_similarity != False:
                return self.wordJoin(name_similarity)
            else:
                return self.wordJoin(random.randrange(self.long))




    def listenAnswer(self) -> str:
        while 1:
            y=self.stt_server(short_str=False)
            if 'yes' in y.result_str:
                self.tts_server('OK.')
                return 'yes'
            elif 'no' in y.result_str:
                return 'no'


    def matchedSearch(self,dict_key1:str, dict_key2:str, information_1:list, information_2:list, num:int) -> (str,bool):

        if set(information_1) & set(self.dict[dict_key1][num]) and set(information_2) & set(self.dict[dict_key2][num]):
            return self.wordJoin(num)
        else:
            return False

    #類似度がもっとも高いものを探す
    def matchedWord2vec(self,dict_key1:str,information_1:str) -> (int,bool):
        defalt=0.0
        correct=0 #要素数
        succese=False
        #tryはword2vecに存在しない単語の場合エラーが出るため
        try:
            for na in information_1:
                for ob in range(self.long):
                    for ob_na in self.dict[dict_key1][ob]:
                        value= word_vectors.similarity(na,ob_na)
                        if value>minimum_value and defalt<value:
                            defalt=value
                            correct=ob
                            succese=True
            if succese:
                return correct
            else:
                return False
        except:
            return False


    def wordJoin(self,correct:int) -> str:
        self.tts_server('I will go '+' '.join(self.dict['place_feature'][correct]) +' '.join(self.dict['place_name'][correct])+' is this  OK?')
        if self.listenAnswer()==False:
            return 'no'
        if self.dict['place_feature'][correct]:
            return ' '.join(self.dict['place_feature'][correct]) +' '+' '.join(self.dict['place_name'][correct])
        else:
            return ' '.join(self.dict['place_name'][correct])




if __name__=='__main__':
    rospy.init_node('test_phase')
    ggi=GgiTest()
    rospy.spin()
