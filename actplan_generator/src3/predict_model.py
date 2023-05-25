import json
import dill 
import MeCab
import nltk
import re
MODEL_PATH = "../resource/src3/"
#svc
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
#crf
import sklearn_crfsuite
from train_model_crf import sent2features, word2features, sent2labels


#モデルの読み込み(crf)
with open(MODEL_PATH+"crf.model", "rb") as f:
    crf = dill.load(f)

#モデルの読み込み(svm)
with open(MODEL_PATH + "svc.model", "rb") as f:
    vectorizer = dill.load(f)
    label_encoder = dill.load(f)
    svc =dill.load(f)
    

def split_and_pos(sen):
    morph = nltk.word_tokenize(sen)   #分かち書き)
    pos =  nltk.pos_tag(morph) #品詞の取得
    return pos

def extract_crf(utt):
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
    
def extract_svc(utt):
    words = []
    lines = split_and_pos(utt)
    for line in range(len(lines)):
        if line == "EOS":
            break
        else:
            word = lines[line][0]
            feature_str = lines[line][1]
            words.append(word)
            
    tokens_str = " ".join(words)
    X = vectorizer.transform([tokens_str])
    Y = svc.predict(X)
    da = label_encoder.inverse_transform(Y)[0]
    return da


if __name__ == "__main__":
    #for utt in ["could you tell me how many people in the guestroom"]:
    sentence = r"Tell your team's name to Robin at the shelf"
    pattern = '[a-zA-Z0-9_] name'
    
    result = re.findall(pattern,sentence,re.S)
    print(type(result))
    for utt in []: 
        conceptdic = extract_crf(utt)
        da = extract_svc(utt)
        #print(utt)
        #print(conceptdic)
        #print(da)
        print(da, ":",utt,conceptdic)
