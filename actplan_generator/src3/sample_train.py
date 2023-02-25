import sklearn_crfsuite
#from crf_util import word2fetures, sent2features, sent2labels
import dill 
import MeCab
import nltk

mecab = MeCab.Tagger()
mecab.parse('')

SENTS = []
LIS = []

def word2features(sent,i):
    word = sent[i][0]
    postag = sent[i][1]
    features = {
        'bias':1.0,
        'word':word,
        'postag':postag
    }
    if i > 0:
        word_left = sent[i-1][0]
        postag_left = sent[i-1][1]
        features.update({
            '-1:word':word_left,
            '-1:postag':postag_left
        })
    else: features['BOS'] = True

    if i < len(sent) -1:
        word_right = sent[i+1][0]
        postag_right = sent[i+1][1]
        features.update({
            '+1:word':word_right,
            '+1:postag':postag_right
        })
    else: features['EOS'] = True
    
    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for word, postag, label in sent]

def train_crf(SENTS,LIS):
    for line in open("crf_samples.dat", "r"):
        line = line.rstrip()
        if line == "":
            SENTS.append(LIS)
            LIS = []
        else:
            word,postag,label = line.split('\t')
            LIS.append([word,postag,label])

    X = [sent2features(s) for s in SENTS]
    Y = [sent2labels(s) for s in SENTS]

    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1       =0.1,
        c2       =0.1,
        max_iterations=100,
        all_possible_transitions=False
    )
    crf.fit(X,Y)
    with open("crf.model","wb") as f:
        dill.dump(crf, f)

if __name__ == "__main__":
    train_crf(SENTS,LIS)