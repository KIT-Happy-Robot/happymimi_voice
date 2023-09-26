from transformers import BertTokenizer,DistilBertTokenizer
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from transformers import TFDistilBertForSequenceClassification
from transformers import TFBertModel,TFDistilBertModel

MODEL_NAME="distilbert-base-uncased"
tokenizer = DistilBertTokenizer.from_pretrained(MODEL_NAME)


# テキストのリストを専用の入力データに変換
def to_features(texts, max_length):
    shape = (len(texts), max_length)
    # input_idsやattention_mask, token_type_ids
    input_ids = np.zeros(shape, dtype="int32")
#     attention_mask = np.zeros(shape, dtype="int32")

    for i, text in enumerate(texts):
        encoded_dict = tokenizer.encode_plus(text, max_length=max_length, pad_to_max_length=True,truncation=True)
        input_ids[i] = encoded_dict["input_ids"]
#         attention_mask[i] = encoded_dict["attention_mask"]

    return [tf.cast(input_ids, tf.int32)]