#! /bin/bash
sudo -E apt install portaudio19-dev
pip install -r requirements.txt
DIR=$HOME"/catkin_ws/src/happymimi_voice/config/dataset"
FILE=$DIR"/stanford-tagger-4.2.0.zip" 
MG_FILE=$DIR"glove.twitter.27B.200d.magnitude"
echo $DIR
if [ ! -e $FILE ]; then
  echo "install stanford data"
  wget https://nlp.stanford.edu/software/stanford-tagger-4.2.0.zip
  unzip stanford-tagger-4.2.0.zip
  if [ ! -d $DIR ]; then
    echo -e "\e[31m ~/catkin_ws/src/happymimi_voice/dataset is not find, please clone happymimi_voice \e[m"
  else
    mv stanford-postagger-full-2020-11-17 ~/catkin_ws/src/happymimi_voice/config/dataset/stanford-postagger
  fi
fi
if [ ! -e $MG_FILE]; then
    echo "install glove.twitter.27B.200d.magnitude"
    wget -c http://magnitude.plasticity.ai/glove/heavy/glove.twitter.27B.200d.magnitude
    if [ ! -d $DIR ]; then
        echo -e "\e[31m ~/catkin_ws/src/happymimi_voice/dataset is not find, p      lease clone happymimi_voice \e[m"
  　else
        mv glove.twitter.27B.200d.magnitude ../config/dataset/glove-twitter-27B-200d.magnitude
    fi
fi

python nltk_download.py
python gensim_download.py

