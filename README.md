# Happymimi_voice

## Overview
This package is a collection of the voice processing functions.
(このパッケージは音声関連の機能をまとめています)

## Description
### Features this package has(このパッケージの機能は以下のようになっています。)
- Speech-To-Text and Text-To-Speech by Google api. (writen by ros)

 →(Google APIが提供する「Sppech-To-Text」,「Text-To-Speech」を使用しています（因みにノードはROSで書いてるよ）)
 
- Action_Planning using Morphological Analysis. (GPSR)

 →(形態素解析を使用した行動計画を行います。 （「GPSR」ていう競技で使うよ）)
 
- Predict the gender from name.

 →（名前から性別を予測することができます。）
 
- Environment teaching function. (GGI)
 
 →（周辺環境の学習機能（「GGI」ていう競技で使うよ））

- Command recognition by voice.

→（音声によるコマンド認識を行います）
  
  etc

### Technology used(使用している技術)
- Speech-To-Text and Text-To-Speech（「Speech-To-Text」,「Text-To-Speech」）
- Morphological Analysis（形態素解析）
- word2vec and cosine similarity used it（「word2vec」を用いたコサイン類似度計算）
- Levenshtein Distance（レーベンシュタイン距離）

## Requirement（環境構築要件）
### システム要件
- 空き容量15GB以上（足りない場合は環境構築時のshファイルを参考に各々適切な学習済みデータをダウンロードすること）
- メモリ8GB

### The libraries used and the versions that have been tested（使用されたライブラリとテストされたバージョン）
```
numpy==1.21.0
pickle5==0.0.11
nltk==3.4.5
google-cloud-speech==2.4.1
google-cloud-texttospeech==2.5.2
rospkg==1.3.0
python-levenshtein
pyaudio==0.2.11
gensim==4.0.1
dill==0.3.4
scikit-learn==0.24.2
ngram==3.3.2
pymagnitude==0.1.143
wheel==0.37.0
fuzzy==1.2.2
spacy==3.1.4
```

## How to build enviroment（環境を構築する方法）
How to the installation of python, pip, etc. is omitted.
It's partly described in esa and if you want to know, please check it.

（python、pipなどのインストール方法は省略しています。
esaに一部記載されていますので、知りたい方はチェックしてみてください。）

https://kithappyrobot.esa.io/posts/166

I recommend using a virtual environment(venv)

（仮想環境（venv）の使用をお勧めします）

### install pyhton3.8（Python3.8のインストール）
python3.8で作成されているものがあるため、以降のバージョンでしか動かない場合がある。
```
sudo apt install python3.8
sudo apt install python3.8-dev
```

### ~install pyhton-venv（Python仮想環境作成用のライブラリインストール）~
※ここはやらなくても良い！
```
sudo apt install python3.8-venv
```

### Set the environment variable to the file path of the service account key（環境変数をサービスアカウントキーのファイルパスに設定します）
:warning: Please make sure you have received your Google service account key in advance.

（警告：事前にGoogleサービスアカウントキーを受け取っていることを確認してください。）

```
export GOOGLE_APPLICATION_CREDENTIALS="/home/<USER>/Downloads/AtHome-f70ff86ec2fd.json"
```
### Install libraries to be used in the package（パッケージで使用するライブラリをインストール）
Get inside this package.

（以下のように行って下さい。）

```
#make venv
python3.8 -m venv envs/venv ※ここはやらなくても良い！
#enter venv
source envs/venv/bin/activate ※ここはやらなくても良い！
#some libraries and data install
cd enviroment_building
sh enviroment.sh

```

### word2vec data install(word2vecで使用するデータのインストール)
※自宅で行うと良い！
```
#8Gぐらいある
wget -c http://magnitude.plasticity.ai/fasttext/heavy/crawl-300d-2M.magnitude
mv crawl-300d-2M.magnitude ../config/dataset/
```
軽い重みを使いたい場合は
https://github.com/plasticityai/magnitude
からダウンロードし名前を変更


### pyThorch
本パッケージではword2vecを高速で扱うためにpymagnitudeを利用しているが、各自の端末に適したpyTorchが必要になる。
以下のリンクからinstallコマンドを生成してインストールを実行してください。
https://pytorch.org/get-started/locally/

### Anticipated errors(予想されるエラー)
```
#ssl error
export https_proxy=http://wwwproxy.kanazawa-it.ac.jp
export HTTPS_PROXY=http://wwwproxy.kanazawa-it.ac.jp
export http_proxy=http://wwwproxy.kanazawa-it.ac.jp
export HTTP_PROXY=http://wwwproxy.kanazawa-it.ac.jp
export ftp_proxy=ftp://wwwproxy.kanazawa-it.ac.jp

#no module wheel
pip install wheel
```
#### sh実行時416 Requested Range Not Satisfiable
sh内のwgetコマンドが原因→理由は不明
直接ダウンロードしてくる必要がある
http://magnitude.plasticity.ai/glove/heavy/glove.twitter.27B.200d.magnitude

## Usage
Write in each package by japanese

(他のパッケージは日本語で書いてるよ)

## EDITER
- 福田 直央(2019年度参加)

## TRANSLATOR
- 奥瀬 皓也（2021年度参加）

