#! /bin/bash
sudo -E apt install portaudio19-dev
pip install -r requirements.txt
DIR=$HOME"/catkin_ws/src/happymimi_voice/config/dataset"
FILE=$DIR"/stanford-tagger-4.2.0.zip" 
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
python nltk_download.py
python gensim_download.py
