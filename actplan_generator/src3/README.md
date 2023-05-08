## Overview
CRF(条件付確率場)を使って行動計画を生成する。現在は200行程度のデータを水増しして学習にかけたが、精度は微妙である。  
データセットの水増しの方法やアノテーションの仕方を変えると精度が上がると思うので各自挑戦すること。  
CRFについて知りたい人は下記のサイトを参考にしてね💛  
[【技術解説】CRF(Conditional Random Fields)](https://mieruca-ai.com/ai/conditional-random-fields/)

---
SVM(サポートベクターマシン)を用いて対話タイプの推定を行う。指示された文章が「ものを持ってくるタスク」「人に伝える」「人を数える」「誰かを部屋に導く」なのか等を推定し、対話行為を分類する。
SVMについて知りたい人は下記のサイトを参考にしてね💘  
[【技術解説】SVM(Support Vector Machine)](https://aiacademy.jp/media/?p=248)
## Description

- ### increase_sentence_crf.py increase_sentence_svm.py
    > 学習用データを水増しする。Magnitudeで類似単語を置き換えるが文章が不適切になる場合がある。

- ### train_model.py train_model_svm.py
    > 学習用データから機械学習を行う。（モデルの構築を自分で行えば、精度伸びそう。今回はライブラリを使用）

- ### predict_model.py
    > 生成されたモデルで推論を行う。

## make dataset & USAGE

1. 整形したデータをexam_crf.txtとexam_svm.txtに保存

exam_crf
```
<nc>could you</nc> <act>tell</act> <human>me</human> how many <target>people</target> in the <location>room</location> are
```

exam_svm
```
da=go_and_give
<act>go</act> to the <location>location</location> <act>find</act> the <target>tray</target> <act>give</act> it to <human>name</human> at the <location>location</location>
```
2. exam_crf.txtの内容は以下のようなアノテーションになっている（内容の変更は可、順番は統一すること）。
- 対応表　

|  tag  |  target  |
|  ----  |  ----  |
| act | {動詞} |
|  target  |  {対象のもの}  |
|  location  |  {場所}  |
|  human  |  {対象の人}  |

※関係ない語句は<nc>としてまとめるといいかも
※tagのつけ方はもう一工夫いる感じする

3. increase_sentence_crf.pyでデータを水増しし、分解してcrf_sentence.datに保存
```
src2$ python3 increase_sentence.py
```
crf_sentence.dat
```
robot	NN	O
please	NN	O
navigate	NN	B-act_0
to	TO	O
.
.
.
```

4. 学習にかける（後々に自分で構築したい）うまくいくと「crf.model」ができるはず
```
python3 train_model.py
```
5. 結果を確認

```
python3 predict_model.py
```
