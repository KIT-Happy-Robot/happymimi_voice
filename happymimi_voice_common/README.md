# happymimi_voice_common
## Overview
音声範囲外も利用する汎用的なノードを含むパッケージ

## Description
以下のノードを含む
- ### listen_command.py 
    > 音声認識からhappymimi_voice/config/listen_cmdにあるファイルのコマンドを認識する

- ### stt_server.py
    > GCPを使った音声認識機能を提供する

- ### tts_srvserver.py
    > GCPを使った音声合成機能を提供する

- ### yes_no.py
    > 音声認識によりyesかnoかを判断する

- ### waveplay_srv.py
    > ttsではネット環境が悪いと再生に時間がかかるため、事前に再生ファイルを作成し再生させる

- ### get_feature_srv.py
    > 音声データからリクエストされた内容を取得する

## Requirement
省略

## Build Environment
省略

## Bring Up
仮想環境に入った後に実行
```
~/happymimi_voice$ source envs/(環境名)/bin/activate 
$ roslaunch happymimi_voice_common voice_common.launch

```
## How to use
基本はUsed msgsに書いてあるので一部のみ記載

- ### waveplay_srv.py
> 再生した音声合成ファイルの指定

#### 音声ファイルの作成方法
```
~/happymimi_voice$ source envs/(環境名)/bin/activate 
~/happymimi_voice_common/src/ python
>>> import waveplay_srv as wav
>>> wav.waveMaker("hello","hello.wav")
```

- ### get_feature_srv.py
> 取得したい情報を指定すると、音声を流し欲しい情報を返す

#### 対応表
| 送信内容 | 受信内容 | 受信種類 |
----|----|---- 
| "name" | "人の名前" | config/voice_common/name.txt参照 |
| "old" | "年齢" | 文字列の数字
| "gender" | "性別" | "woman", "man" |
| "predict gender" | "性別" | "woman","man" ※ |
※名前からナイーブベイズ統計による推論　音声再生はない

## Used msgs
- ### listen_command.py 
#### happymimi_voice_msgs/StringToString.srv
```
string request_data  #コマンドとして使うファイル名
---
string result_data   #成功：'対応したコマンド' 失敗：'' 
bool result	     #成功：True 失敗：False
```

- ### stt_server.py
#### happymimi_voice_msgs/SpeechRecog.srv
```
bool short_str    #扱うものが短い文か長い文か
#以下２つは必要ない場合省略可
string[] context_phrases    #認識しやすくしたい単語のリスト
float32 boost_value         #上記のリストの単語をどのぐらい認識しやすくするか デフォルト 20.0
---
string result_str
```

- ### tts_srvserver.py
#### happymimi_msgs/StrTrg.srv
```
string data  #喋らせたい文字列
---
bool result     
```

- ### yes_no.py
#### happymimi_voice_msgs/YesNo.srv
```
---
bool result #yes:True no:False
```

- ### waveplay_srv.py
#### happymimi_msgs/StrTrg.srv
```
string data   # 再生するファイル（一部パス）
---
bool result   # 再生できたか否か
```

- ### get_feature_srv.py
#### happymimi_voice_msgs/StringToString.srv
```
string request_data  #取得したい情報
---
string result_data   # 取得した情報
bool result	     #成功：True 失敗：False
```


