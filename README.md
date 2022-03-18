# Happymimi_voice

## Overview
This package is a collection of the voice processing functions.
(このパッケージは音声関連の機能をまとめています)

## Description
### Features this package has
- Speech-To-Text and Text-To-Speech by Google api. (writen by ros)
- Action_Planning using Morphological Analysis. (GPSR)
- Predict the gender from name.
- Environment teaching function. (GGI)
- Command recognition by voice.
  etc

### Technology used
- Speech-To-Text and Text-To-Speech
- Morphological Analysis
- word2vec and cosine similarity used it.
- Levenshtein Distance

## Requirement
### システム要件
- 空き容量15GB以上（足りない場合は環境構築時のshファイルを参考に各々適切な学習済みデータをダウンロードすること）
- メモリ8GB

### The libraries used and the versions that have been tested
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

## How to build enviroment
How to the installation of python, pip, etc. is omitted.
It's partly described in esa and if you want to know, please check it.
https://kithappyrobot.esa.io/posts/166

I recommend using a virtual environment(venv)

### install pyhton3.8
python3.8で作成されているものがあるため、以降のバージョンでしか動かない場合がある。
```
sudo apt install python3.8
sudo apt install python3.8-dev
```

### install pyhton-venv
```
sudo apt install python3.8-venv
```

### Set the environment variable to the file path of the service account key
:warning: Please make sure you have received your Google service account key in advance.
```
export GOOGLE_APPLICATION_CREDENTIALS="/home/<USER>/Downloads/AtHome-f70ff86ec2fd.json"
```
### Install libraries to be used in the package
Get inside this package.
```
#make venv
python3.8 -m venv envs/venv
#enter venv
source envs/venv/bin/activate
#some libraries and data install
cd enviroment_building
sh enviroment.sh

```

### word2vec data install
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

### Anticipated errors
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

## Usag
Write in each package by japanese

## EDITER
- 福田 直央(2019年度参加)

