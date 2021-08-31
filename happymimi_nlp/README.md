# Directory where the nodes for natural language processing are located
## gender_judgement_from_name.py
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

## morphological_analysis.py
### 概要
形態素解析を行い、整理するノード
### 使い方
```
>>>import morphological_analysis as ma
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


