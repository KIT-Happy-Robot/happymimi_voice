import gensim.downloader as api
import pickle as pk
import sys
model_name="word2vec-google-news-300"
print("model is %s" % model_name)
if input("Do you want to run?(y/n):") in 'y':
    pass
else:
    print("stop")
    sys.exit()

class_list=["food","drink","bottle"]
file_path=os.path.expanduser('~/catkin_ws/src/voice_common_pkg/config')
max_word=100 #汎化する用語の最大数
minimum_evaluation_value=0.5 #最小評価値
model=api.load("word2vec-google-news-300")
add_word=[]
dict_class={}

for c in class_list:
    for word,value in model.most_similar([c],topn=max_word):
        #print(word, value)
        if value >= minimum_evaluation_value:
            add_word.append(word)
    dict_class[c]=set(add_word)
    add_word=[]
print(dict_class)
with open(file_path+"class_by_word2vec.pkl","wb") as f:
    pk.dump(dict_class,f)
