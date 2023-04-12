import json
import dill 
import MeCab
import nltk
import sklearn_crfsuite
from train_model import sent2features, word2features, sent2labels
import re


with open("crf.model", "rb") as f:
    crf = dill.load(f)

def split_and_pos(sen):
    morph = nltk.word_tokenize(sen)   #分かち書き)
    pos =  nltk.pos_tag(morph) #品詞の取得
    return pos

def extract(utt):
    lis = []
    #for line in mecab.parse(utt).splitlines():
    lines = split_and_pos(utt)
    for line in range(len(lines)):
        word = lines[line][0]
        postag = lines[line][1]
        lis.append([word, postag, "O"])
        
    
    words = [x[0] for x in lis]
    X = [sent2features(s) for s in [lis]]
    labels = crf.predict(X)[0]
    
    conceptdic = {}
    buf = ""
    last_label = ""
    for word, label in zip(words, labels):
        if re.search(r'^B-', label):
            if buf != "":
                _label = last_label.replace('B-','').replace('I-','')
                conceptdic[_label] = buf
            buf = word
        elif re.search(r'^I-', label):
            buf += word
        elif label == "O":
            if buf != "":
                _label = last_label.replace('B-','').replace('I-','')
                conceptdic[_label] = buf
                buf = ""
        last_label = label
        
    if buf != "":
        _label = last_label.replace('B-','').replace('I-','')
        conceptdic[_label] = buf
        
    return conceptdic
    
        
if __name__ == "__main__":
    for utt in ["could you tell me how many people in the guestroom"]:
        conceptdic = extract(utt)
        print(utt, conceptdic)