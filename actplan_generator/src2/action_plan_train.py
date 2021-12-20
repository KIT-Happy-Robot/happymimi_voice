# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow import keras
import numpy as np
import sys
import time

sys.path.append('..')
from happymimi_nlp import data_operation
from happymimi_nlp.Attention_Model import *
#datasetのロード
#print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))


data_class=data_operation.DataOperation(input_id="../resource/input_id.txt",output_id="../resource/output_id.txt")
(input_train,input_test) , (output_train , output_test) = data_class.data_load()
targ_lang,targ_num=data_class.word_dict()
split_num=1
BUFFER_SIZE = len(input_train)
BATCH_SIZE = int(20)
steps_per_epoch = len(input_train)//BATCH_SIZE
embedding_dim = int(256/8)
units = int(1024/10)

#datasetをバッチに分解
dataset = tf.data.Dataset.from_tensor_slices((input_train, output_train)).shuffle(BUFFER_SIZE)
dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)

#このデータを何回学習させるか
EPOCHS = 10

#encoderとdecorderを定義  get_sizeは後で変更
encoder = Encoder(data_class.get_size(), embedding_dim, units, BATCH_SIZE,len(input_train[0]))
decoder = Decoder(data_class.get_size(), embedding_dim, units, BATCH_SIZE,len(output_train[0]))
del data_class
#使う最適化アルゴリズムと損失関数を定義
optimizer = tf.keras.optimizers.Adam()
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=True, reduction='none')

#保存するための変数を定義
checkpoint_dir = '../../config/dataset/training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(optimizer=optimizer,
                                 encoder=encoder,
                                 decoder=decoder)


#損失関数とオプティマイザ
def loss_function(real, pred):
    mask = tf.math.logical_not(tf.math.equal(real, 0)) #equal:real==0の真理値 logical_not : 真理値の逆を返す
    loss_ = loss_object(real, pred)    # 交差エントロピー誤差

    mask = tf.cast(mask, dtype=loss_.dtype)  #
    loss_ *= mask

    return tf.reduce_mean(loss_)

#inp:batch input targ: batch output
def train_step(inp, targ, enc_hidden):
    loss = 0
    change_word=lambda x:[targ_num[int(i)] for i in x.split()]
    #自動微分できるようにする
    with tf.GradientTape() as tape:
        #内部情報、最後の出力
        enc_output, enc_hidden = encoder(list(map(change_word,inp)), enc_hidden)

        dec_hidden = enc_hidden
        #batchsize分用意する
        dec_input = tf.expand_dims([targ_lang['<start>']] * BATCH_SIZE, 1)

        # Teacher Forcing - 正解値を次の入力として供給
        for t in range(1, targ.shape[1]):
            # passing enc_output to the decoder    (start, encorderの最後の出力, encorderの内部情報)2,3引数はattentionにも使う
            predictions, dec_hidden, _ = decoder(dec_input, dec_hidden, enc_output)

            loss += loss_function(targ[:, t], predictions)

            # Teacher Forcing を使用
            #1ずつずらす
            dec_input = tf.expand_dims(targ[:, t], 1)

    batch_loss = (loss / int(targ.shape[1]))

    variables = encoder.trainable_variables + decoder.trainable_variables

    gradients = tape.gradient(loss, variables)

    optimizer.apply_gradients(zip(gradients, variables))#adam

    return batch_loss


if __name__=="__main__":
    print("start trainning")
    for epoch in range(EPOCHS):
        start = time.time()

        enc_hidden = encoder.initialize_hidden_state() #zeroの行列
        total_loss = 0
        # inp:input data targ: output data (バッチ単位)
        for (batch, (inp, targ)) in enumerate(dataset.take(steps_per_epoch)):
            batch_loss = train_step(inp, targ, enc_hidden)
            total_loss += batch_loss

            if batch % 100 == 0:
                print('Epoch {} Batch {} Loss {:.4f}'.format(epoch + 1,
                                                         batch,
                                                         batch_loss.numpy()))
      # 2 エポックごとにモデル（のチェックポイント）を保存
        if (epoch + 1) % 2 == 0:
            checkpoint.save(file_prefix = checkpoint_prefix)

        print('Epoch {} Loss {:.4f}'.format(epoch + 1,
                                          total_loss / steps_per_epoch))
        print('Time taken for 1 epoch {} sec\n'.format(time.time() - start))
