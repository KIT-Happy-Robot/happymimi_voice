#! /usr/bin/env python
# -*- coding: utf-8 -*-


from pymagnitude import Magnitude as mag
import os.path

file_path=os.path.expanduser('~/catkin_ws/src/happymimi_voice/config/dataset')

class Word2vecMagnitude():
    def __init__(self,data_file="/crawl-300d-2M.magnitude"):
        print(file_path+data_file)
        self.word_vectors=mag(file_path+data_file)

    def searchCloseWord(self,target,search_ls,threshold=0.6):
        succese=False
        #tryはword2vecに存在しない単語の場合エラーが出るため
        for comp in search_ls:
            try:
                value= self.word_vectors.similarity(target,comp)
                if threshold<value:
                    threshold=value
                    correct=comp
                    succese=True
            except:
                print("not found "+comp)
                pass
        if succese:
            return correct
        else:
            return None


if __name__=="__main__":
    mg=Word2vecMagnitude()
    #i=input("name>>")
    '''
    i="find"
    command_ls=["go", "grasp", "search", "speak", "give", "place", "approach"]
    add_com=["follow"]
    command_ls=command_ls+add_com
    print(mg.searchCloseWord(i,command_ls))
    '''
    print(mg.word_vectors.similarity("life","money"))
