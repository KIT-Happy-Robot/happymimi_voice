# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
from pymagnitude import Magnitude
from pymagnitude import MagnitudeUtils

import numpy 
import threading
#magnitudeのデータは少し読み込みに時間がかかる
#並列処理で読み込みを待つ

file_path = os.path.expanduser('~/catkin_ws/src/happymimi_voice/config/dataset/')
file_mg = file_path + 'wiki-news-300d-1M-subword.magnitude'

magnitude_data = Magnitude(file_mg)
#vecs = Magnitude(MagnitudeUtils.download_model(file_mg))
"""
def get_embedding(embedding,x):
    main_tf=[]
    print(embedding)
    for sentence in x:
        sub_tf=[]
        for word in sentence:
            sub_tf.append(embedding[word][0])
        main_tf.append(sub_tf)
    print(main_tf)
    return tf.constant(main_tf)
"""
def get_embedding(embedding,x):
    main_tf=[]
    print(embedding)
    for sentence in x:
        sub_tf=[]
        for i in range(len(embedding)):
            sub_tf.append(embedding[i][0])
        main_tf.append(sub_tf)
    print(main_tf)
    return tf.constant(main_tf)


class Encoder(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, enc_units, batch_sz,input_length):
        super(Encoder, self).__init__() #オーバーライドするため
        self.batch_sz = batch_sz
        self.enc_units = enc_units
        # self.embedding = tf.keras.layers.Embedding(vocab_size,
                        # embedding_dim,input_length=input_length)
        # self.embedding=mag("../../config/dataset/crawl-300d-2M.magnitude")

        self.embedding = magnitude_data
        self.gru = tf.keras.layers.GRU(self.enc_units,
                                       return_sequences=True,
                                       return_state=True,
                                       recurrent_initializer='glorot_uniform')#Glorot の一様分布（Xavier の一様分布とも呼ばれます）による初期化を返します

    def call(self, x, hidden):
        x1= get_embedding(self.embedding,x)
        # print("embed shape:"+str(x.shape))
        output, state = self.gru(x1, initial_state = hidden)
        return output, state

    def initialize_hidden_state(self):
        return tf.zeros((self.batch_sz, self.enc_units)) #batch*enc_unitsのゼロの行列

##
class BahdanauAttention(tf.keras.layers.Layer):
    def __init__(self, units):
        super(BahdanauAttention, self).__init__()
        self.W1 = tf.keras.layers.Dense(units)
        self.W2 = tf.keras.layers.Dense(units)
        self.V = tf.keras.layers.Dense(1)
    def call(self, query, values):
        # hidden shape == (batch_size, hidden size)
        # hidden_with_time_axis shape == (batch_size, 1, hidden size)
        # 次元数を合わせないと加算できない
        hidden_with_time_axis = tf.expand_dims(query, 1)

        # score shape == (batch_size, max_length, 1)
        # スコアを self.V に適用するために最後の軸は 1 となる
        # self.V に適用する前のテンソルの shape は  (batch_size, max_length, units)
        #print("shape")
        #print(values.shape,hidden_with_time_axis.shape)
        w1=self.W1(values)
        w2=self.W2(hidden_with_time_axis)
        score = self.V(tf.nn.tanh(
            w1 + w2))

        # attention_weights の shape == (batch_size, max_length, 1)
        attention_weights = tf.nn.softmax(score, axis=1)

        # context_vector の合計後の shape == (batch_size, hidden_size)
        context_vector = attention_weights * values#それぞれの割合をかける
        context_vector = tf.reduce_sum(context_vector, axis=1)# 割合の大きい単語が色濃く出てるベクトルになる

        return context_vector, attention_weights


class Decoder(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, dec_units, batch_sz,output_length):
        super(Decoder, self).__init__()
        self.batch_sz = batch_sz
        self.dec_units = dec_units
        # self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim,input_length=output_length)
        #self.embedding=Magnitude(file_mg)
        self.embedding = magnitude_data
        self.gru = tf.keras.layers.GRU(self.dec_units,
                                       return_sequences=True,
                                       return_state=True,
                                       recurrent_initializer='glorot_uniform')
        self.fc = tf.keras.layers.Dense(vocab_size)

        # アテンションのため
        self.attention = BahdanauAttention(self.dec_units)
    #x:はじめ＜start＞
    def call(self, x, hidden, enc_output):
        # enc_output の shape == (batch_size, max_length, hidden_size)
        #attentionを適応したベクトル,単語の割合(確率)
        context_vector, attention_weights = self.attention(hidden, enc_output)

        # 埋め込み層を通過したあとの x の shape  == (batch_size, 1, embedding_dim)
        x = get_embedding(self.embedding,x)

        # 結合後の x の shape == (batch_size, 1, embedding_dim + hidden_size)
        x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=-1)

        # 結合したベクトルを GRU 層に渡す
        output, state = self.gru(x)

        # output shape == (batch_size * 1, hidden_size)
        output = tf.reshape(output, (-1, output.shape[2]))

        # output shape == (batch_size, vocab)
        x = self.fc(output)

        return x, state, attention_weights
