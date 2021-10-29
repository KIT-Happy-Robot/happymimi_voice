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

## Used msgs
- ### listen_command.py 
ListenCommand.srv
```
string file_name  #コマンドとして使うファイル名
---
string cmd        #成功：'対応したコマンド' 失敗：'' 
bool result	  #成功：True 失敗：False
```

- ### stt_server.py
SpeechRecog.srv
```
---
string result   #認識結果の文字列
```

- ### tts_srvserver.py
TTS.srv
```
string sentence  #喋らせたい文字列
---
bool success     #削除予定（すべてFalse）
```

- ### yes_no.py
YesNo.srv
```

---
bool result #yes:True no:False
```


