
:warning: 未完成かつデバッグできてないためおそらくエラーがたくさん出ます。まずはアノテーションは少量で正常に動作するようにすること
## Overview
Attentionモデルを使って行動計画を生成する。アノテーションに時間がかかるため、デバッグできていない（syntaxエラーも含め）。ここに記述するのは理想であり、動作を確認したわけではない
参考程度に利用してください
https://kithappyrobot.esa.io/posts/97

## Description

- ### action_plan_train.py
    > Attentionモデルで行動計画を生成する学習をする。作ったがデバッグできていない

- ### decord_talk.py
    > 学習データのテストを行う。デバッグできていない

- ### dataset_maker.py
    > 学習用データを整形する学習できる形に変換するプログラム。デバッグはしてない

## make dataset

1. 作った整形するための文をsequence.txtの名前にしてコピーする
```
~resource$ cp cat[number]_dataset.txt sequence.txt
```
2. sequence.txtの内容を以下のようなアノテーションの内容に変更する（内容の変更は可、順番は統一すること）。アノテーション次第で精度は変わるため試行錯誤が必要
- 対応表　
|  tag  |  target  |
|  ----  |  ----  |
| action | {動詞} |
|  target  |  {対象のもの}  |
|  location  |  {場所}  |
|  target  |  {対象の人}  |

※ない場合はNone
※ すべて１単語 sayの場合は答えと対応付できる単語
- sequence.txt
```
input: Say something about yourself to the person {gesture} in the {room}
output: say yourself {room} {person}  #gestureは対応が必要、対応表の項目増やすのもあり
input: Please escort {name} to the {location}, you will find him at the {location}
output: escort {name} {location} None find him {location} None #対象は人だが動詞の対象が人であるため問題ないと思う
input: Please meet {name} at the {location} and accompany him to the {location}
output: meet {name} {location} None accompany him {location} None
input: Robot please find three {category} in the {room}
output: find {category} {room} None #threeに対応するように思考すべし

etc...
```
3. dataset_makerを使って単語とidの辞書とinput,outputを分割したファイル、それぞれをidに直したファイルを出力({}を実際のオブジェクト等に置き換えて水増ししたほうがいい)
```
src2$ python dataset_maker.py
```
4. 学習にかける(happymimi_nlp/AttentionModel.pyのembedding処理をword2vecで代用しているため、エラーがでるかも)
```
python action_plan_train.py
```
5. decordして学習結果を確認する

```
python decord_talk.py
input: Robot please find three {category} in the {room}
response: find {category} {room} None
```

