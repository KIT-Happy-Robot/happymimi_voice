# Happymimi_voice

## Overview
This package is a collection of the voice processing functions.

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
```

## How to build enviroment
How to the installation of python, pip, etc. is omitted.
It's partly described in esa and if you want to know, please check it.
https://kithappyrobot.esa.io/posts/166

I recommend using a virtual environment(venv)

### install pyhton-venv
```
sudo apt install python3-venv
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
python3 -m venv envs/venv
#enter venv
source envs/venv/bin/activate
#some libraries and data install
cd enviroment_building
sh enviroment.sh
```

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

## Usag
Write in each package by japanese
