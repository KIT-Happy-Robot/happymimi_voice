# Actplan_Generator

## Overview
GPSR等の文章から行動計画を生成する機能を提供する

## Description
- ### resource
    > このパッケージで使うデータや生成されたデータを配置する。また、RoboCup@Homeの公式コマンドジェネレーターも配置する

- ### src/category12_exfile.py
    > 提供されたコマンドジェネレーターから文の一覧を作成したり、例文を作成したする

- ### src/planning_srv.py
    > 行動計画のサービスサーバーの機能を持つ

- ### src/sentence_parsing.py
    > 文章を解析し行動計画を組むモジュール

- ### src2/action_plan_train.py
    > Attentionモデルで行動計画を生成する学習をする。作ったがデバッグできていない

- ### src2/decord_talk.py
    > 学習データのテストを行う。デバッグできていない

- ### src2/dataset_maker.py
    > 学習用データを整形する学習できる形に変換するプログラム。デバッグはしてない

## Requirement
happymimi_voiceと同様

## Build Environment
省略

## Bring Up
仮想環境に入った後に実行
```
~/happymimi_voice$ source envs/(環境名)/bin/activate
$ roslaunch happymimi_voice_common voice_common.launch
$ rosrun actplan_generator /planning_srv

```

## Used msgs
- ### plannning_srv.py
ActionPlan.srv
```
---
bool result	#成功：True　失敗：False
string[] action	#行動コマンドのリスト
string[] data	#行動のターゲット
```

## How to use

- ### src/category12_exfile.py
```
#プログラムをコマンドジェネレーターにコピー
cp category12_exfile.py ../resource/GPSRCmdGen
#データセット作成
##category1
python3 category12_exfile.py dataset1
mv cat1_dataset.txt ../
##category2
python3 category12_exfile.py dataset2
mv cat2_dataset.txt ../
##category12
python3 category12_exfile.py dataset12
mv cat12_dataset.txt ../



#例文作成
##category1
python3 category12_exfile.py ex1
##category2
python3 category12_exfile.py ex2
mv cat1_ex.txt ../
mv cat2_ex.txt ../

```

- ### src/sentence_parsing.py
```
#行動計画デバッグ(仮想環境内)
~/src$ python sentence_parsing.py
#~/resorce$に２つのファイルが作成される success_question.txt(行動計画生成成功) fail.log(生成失敗)
```
- #### 失敗する原因
  >     - 不完全な文（場所情報が抜けている）
	- xmlに存在しないオブジェクトや場所が含まれている

- ### src/planning_srv.py
```
rosrun actplan_generator planning_srv.py
```
- ### src2はsrc2/READMEを参照

### Technology used
- Speech-To-Text and Text-To-Speech
- 自然言語処理
- レーベンシュタイン距離

## comment and memo
いま実装されているものは出題されるすべての動詞に対して設定を行わなければならないため汎用性が低い。形態素解析とword2vecを用いた類似度計算で行動計画を組んでいたが形態素解析の不確実性（誤認識）が発覚しかつ時間がなかったため断念した。spacyとかAttentionモデルとか調べてみるといいかも
