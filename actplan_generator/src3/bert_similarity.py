from transformers import BertJapaneseTokenizer, BertModel
from sentence_transformers import SentenceTransformer
from sentence_transformers import models 
import torch
import numpy as np

#MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'
MODEL_NAME = 'bert-base-uncased'

tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME)


def sentence_to_vector(model, tokenizer, sentence):
 
  # 文を単語に区切って数字にラベル化
  tokens = tokenizer.encode(sentence, add_special_tokens=True)#<meta charset="utf-8">［"input_ids"]
  # BERTモデルの処理のためtensor型に変換
  input = torch.tensor(tokens).reshape(1,-1)
  # BERTモデルに入力し文のベクトルを取得
  with torch.no_grad():
    outputs = model(input, output_hidden_states=True)
    last_hidden_state = outputs.last_hidden_state[0]#<meta charset="utf-8">［0]
    averaged_hidden_state = last_hidden_state.sum(dim=0) / len(last_hidden_state) 
 
  return averaged_hidden_state


def calc_similarity(sentence1, sentence2):
  print("{}".format(sentence1))
  
  sentence_vector1 = sentence_to_vector(model, tokenizer, sentence1)
  sentence_vector2 = sentence_to_vector(model, tokenizer, sentence2)
 
  score = torch.nn.functional.cosine_similarity(sentence_vector1, sentence_vector2, dim=0).detach().numpy().copy()
  print(sentence2,"類似度：", score)
  
sentence1 = "Go"
#sentence2 = "get"
#calc_similarity(sentence1, sentence2)

def most_similarity(text):
    text_list = ["go","navigate","tell","grasp","get"]
    for i in range(len(text_list)):
        calc_similarity(text, text_list[i])
        
most_similarity(sentence1)