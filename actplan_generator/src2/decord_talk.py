# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow import keras
import numpy as np
import sys
import time
import MeCab
import re

sys.path.append('..')
from common import data_operation
from common.Attention_Model import *

max_output=100
data_class=data_operation.DataOperation()
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
encoder = Encoder(data_class.get_size(), embedding_dim, units, BATCH_SIZE,len(input_train[0]))
decoder = Decoder(data_class.get_size(), embedding_dim, units, BATCH_SIZE,len(output_train[0]))

#使う最適化アルゴリズム
optimizer = tf.keras.optimizers.Adam()


#保存するための変数を定義
checkpoint_dir = '../../learn_data/training_checkpoints_en'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(optimizer=optimizer,
                                 encoder=encoder,
                                 decoder=decoder)

checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))
#.assert_consumed()
#正規化
def preprocess_sentence(str):
    wakati = MeCab.Tagger("-Owakati")
    #print(str)
    str2=re.sub("\（.+?\）", "", str)
    str3=re.sub("[A-Z]\d*","human",str2)
    str4=re.sub(r"[,.!?:;' ]", "",str3)
    return "<start> "+wakati.parse(str4).replace("\n","")+"<end>"


def evaluate(sentence,Jp_=True):
    try:
        if Jp_:
            sentence = preprocess_sentence(sentence)
        else:
            sentence=sentence.replace("."," .").replace("?", " ?").replace("!"," !")
        print(sentence,sentence.split(' '))
        inputs = [targ_lang[i] for i in sentence.split(' ')]
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
    enc_out, enc_hidden = encoder(inputs, hidden)

    dec_hidden = enc_hidden
    dec_input = tf.expand_dims([targ_lang['<start>']], 0)

    for t in range(max_output):
        predictions, dec_hidden,_  = decoder(dec_input,
                                            dec_hidden,
                                             enc_out)

        predicted_id = tf.argmax(predictions[0]).numpy()

        result += targ_num[predicted_id] + ' '

        if targ_num[predicted_id] == '<end>':
            return result, sentence

        # 予測された ID がモデルに戻される
        dec_input = tf.expand_dims([predicted_id], 0)

    return result, sentence





if __name__=='__main__':
    while(1):
        str=input("input:")
        result, sentence = evaluate(str,Jp_=False)

        print('response: {}'.format(result))
