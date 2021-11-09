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
---
string result   #認識結果の文字列
```

- ### tts_srvserver.py
> 喋らせたい文字列を渡すと音声合成が再生される

- ### yes_no.py
> 呼び出すのみ

- ### waveplay_srv.py
> 再生した音声合成ファイルの指定

- ### get_feature_srv.py
> 取得したい情報を指定すると、音声を流し欲しい情報を返す
| 送信内容 | 受信内容 | 受信種類 |
----|----|---- 
| "name" | "人の名前" | config/voice_common/name.txt参照 |
| "old" | "年齢" | 文字列の数字
| "gender" | "性別" | "woman", "man" |
| "predict gender" | "性別" | "woman","man" ※ |
※ナイーブベイズ統計による推論　音声再生はない
```
string request_data  #取得したい情報
---
string result_data   # 取得した情報
bool result	     #成功：True 失敗：False
```

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
---
string result   #認識結果の文字列
```

- ### tts_srvserver.py
#### happymimi_msgs/StrTrg.srv
```
string data  #喋らせたい文字列
---
bool result     #削除予定（すべてFalse）
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


