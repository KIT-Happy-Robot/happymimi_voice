# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow import keras
import numpy as np
import sys
import time
import MeCab
import re
from pymagnitude import *
from action_plan_train import checkpoint

sys.path.append('../../')
from happymimi_nlp import data_operation
from happymimi_nlp.Attention_Model import *

file_path = os.path.expanduser('~/Downloads/')
file_mg = file_path + 'crawl-300d-2M.magnitude'
print("now loading..")
magnitude_data = Magnitude(file_mg)


max_output=10
data_class=data_operation.DataOperation(input_id="../resource/input_id.txt",output_id="../resource/output_id.txt")
(input_train,input_test) , (output_train , output_test) = data_class.data_load()
targ_lang,targ_num=data_class.word_dict()

BUFFER_SIZE = len(input_train)
BATCH_SIZE = int(20)
steps_per_epoch = len(input_train)//BATCH_SIZE
embedding_dim = int(256/8)
#embedding_dim=64
units = int(1024/10)

#datasetをバッチに分解
dataset = tf.data.Dataset.from_tensor_slices((input_train, output_train)).shuffle(BUFFER_SIZE)
dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)



#encoderとdecorderを定義  get_sizeは後で変更
encoder = Encoder(data_class.get_size(), embedding_dim, units, BATCH_SIZE,len(input_train[0]),magnitude_data)
decoder = Decoder(data_class.get_size(), embedding_dim, units, BATCH_SIZE,len(output_train[0]),magnitude_data)

#使う最適化アルゴリズム
optimizer = tf.keras.optimizers.Adam()


checkpoint_dir = '../../config/dataset/training_checkpoints'

#チェックポイントをロード（学習済みモデル）
checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))
#.assert_consumed()
#前処理
def sentenceSplit(sentence):
    sentence_ls=[]
    #sentence=re.sub("\（.+?\）", "", sentence)
    #sentence=re.sub("[A-Z]\d+","human",sentence)
    #sentence=re.sub(r"[.!?:;' ]", "",sentence)
    #sentence=re.sub(r"＊+","human",sentence)
    #print(sentence)
    str_ls=sentence.split()
    print("str_ls:",str_ls)
    delimiter_ls=[i for i,x in enumerate(str_ls) if "," in x or "and" in x]
    print("delimiter_ls:",delimiter_ls)
    for i,num in enumerate(delimiter_ls):
        if i==0:
            if "and" in str_ls[num]:
                sentence_ls.append(str_ls[:num])
            else:
                str_ls[num]=str_ls[num].replace(",","")
                sentence_ls.append(str_ls[:num+1])
        else:
            str_ls[num]=str_ls[num].replace(",","")
            if len(delimiter_ls)-1 != i:
                sentence_ls.append(str_ls[num+1:delimiter_ls[i+1]])
            else:
                sentence_ls.append(str_ls[num+1:])


    return sentence_ls



def evaluate(sentence):
    try:
        inputs = []
        sentence=sentenceSplit(sentence)
        #print(sentence,sentence.split(' '))
        print(sentence)
        #inputs = [targ_lang[i] for i in sentence.split(' ')]
        for i in range(len(sentence)):
            inputs.append(targ_lang[i])
            
        inputs = tf.keras.preprocessing.sequence.pad_sequences([inputs],
                                                           value=targ_lang["<PAD>"],
                                                           maxlen=len(input_train[0]),
                                                           padding='post')
    except KeyError as e:
        print(e)
        print("登録済みの単語ではありません")
        sys.exit()

    #tensorにする
    inputs = tf.convert_to_tensor(inputs)
    result = ''

    hidden = [tf.zeros((1, units))]
    print(inputs.shape)
    enc_out, enc_hidden = encoder.call(inputs, hidden)

    dec_hidden = enc_hidden
    dec_input = tf.expand_dims([targ_lang['<start>']], 0)
    
    
    for t in range(max_output):
        predictions, dec_hidden,_  = decoder.call(dec_input,dec_hidden,enc_out)
        
        predicted_id = tf.argmax(predictions[0]).numpy()
        result += targ_num[predicted_id] + ' '

        #if targ_num[predicted_id] == '<end>':
        #    return result, sentence

        # 予測された ID がモデルに戻される
        dec_input = tf.expand_dims([predicted_id], 0)

    return result, sentence





if __name__=='__main__':
    #while(1):
    str="robot please navigate to the kitchen go for a Oliver speak a month"
    result, sentence = evaluate(str)

    print('response: {}'.format(result))
