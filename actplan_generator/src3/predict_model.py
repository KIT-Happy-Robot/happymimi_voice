import Mecab
import json
import dill
import sklearn_crfsuite
import re

mecab = MeCab.Tagger()
mecab.parse("")

with open("crf.model","rb") as f:
    crf = dill.load(f)
    
def extract_concept(utt):
    