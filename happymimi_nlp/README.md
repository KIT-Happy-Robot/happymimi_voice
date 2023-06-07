# Directory where the nodes for natural language processing are located
## other/gender_judgement_from_name.py
### 概要
機械学習を使って名前から性別を予想する
### 使い方
#### ナイーブベイズ分類器
##### 学習をかける場合
```
>>>import gender_judgement_from_name as gj
#学習をかける　名前の頭と真ん中、最後の文字数をパラメータで指定できる
#ハイパーパラメータdefault : first_num=2,midle_num=1,last_num=1 (引数で指定可能)
>>>classifier=gj.GenderJudgementFromNameByNBC.trainNBCmodel()

#予想の正答率の確認(retrun None)
>>>classifier.confirmAccuracy()
test1:0.79
test2:0.80

#名前から性別の予想
>>>classfier.expectGender("anna")
female

#学習モデルの保存
>>>classfier.save(file_path="./genderNBCmodel.dill")

```
##### 保存した学習モデルのロード
```
>>>import gender_judgement_from_name as gj
#モデルのロード
>>>classifier=gj.GenderJudgementFromNameByNBC.loadNBCmodel(file_path="./genderNBCmodel.dill")

#学習をかけた際と同様に扱える
```

## other/sentence_analysis.py
### 概要
文解析系の機能を持つ。（morphological_analysisも統合したほうがいい）
#### wordVerificationメソッド
リストから単語の距離が最も近いものを探す
##### 引数
|  引数名  |  内容  |
| ---- | ---- |
|  word:str  |  対象の単語  |
|  com_ls:list  |  単語のリスト  |
|  default_v=0.6  |  レーベンシュタイン距離の閾値  |
|  fuz=False  |  DMetaphoneを使うか否か  |
|  get_value=False  |  評価値を返すか否か  |

###### 返り値
最も近い単語の要素番号

#### MorphologicalAnalysisクラス
もともとmorphological_analysis.pyにあるやつ
:warning: spacy適応したいけどできてない
```
>>>import sentence_analysis as ma
>>>morp=ma.MorphologicalAnalysis()
#形態素解析の記号割当を確認する
>>>morp.infoTag()
CC	Coordinating conjunction 調整接続詞
CD	Cardinal number	基数
.......略
>>>sentence="Take the bottle from the bath room and give it to iida at the bed room."
>>>morp.getActionplan(sentence)
["go","take","go","give"],["bath room","bottle","bed room","iida"]
```
## actplan/Attention_Model.py
embedding層をword2vecに置き換えたAttentionモデル
使い方は省略
actplan_generatorのsrc2/_action_plan_train.pyを参照

## actplan/data_operation.py
データを学習できる形式に変換してloadするプログラム
```
data_class=data_operation.DataOperation(input_id="../resource/input_id.txt",output_id="../resource/output_id.txt")
(input_train,input_test) , (output_train , output_test) = data_class.data_load()
```

## vv_chatbot/chat_bot.py
chatgptのAPIを用いて簡易的なチャットボットを実現するプログラム
```
prerequisite_en = [{"role": "system", "content" :"You are Happy Mimi, a lifestyle support robot. Your job is to support people in their daily lives. Your master has asked you to be conversation partner. Please answer as many questions as you can."}]
    prerequisite_jp = [{"role": "system", "content" :"あなたは、生活支援ロボット「ハッピーミミ」です。あなたの仕事は、人々の生活をサポートすることです。ご主人様から、会話の相手を頼まれました。できる限り多くの質問に答えてください。また語尾は「~だよ」「~なんだ」で答えて。また、あなたのマスターは鷲尾ひろとです。"}]
    #response = Simple_Response(prerequisite_jp)
    model = prerequisite_jp
    #while True:
    prompt = input("Enter your prompt: ")
    if prompt == "stop" or prompt == "STOP":
        return None
    else:
        model.append({'role': 'user', 'content': prompt}) 
        result_word = Simple_Response(model)
        result = "mimi:" + result_word
        
    print(result) 
```


