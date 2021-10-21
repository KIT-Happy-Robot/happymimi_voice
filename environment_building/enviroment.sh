#! /bin/bash
sudo -E apt install portaudio19-dev
pip install -r requirements.txt
DIR=$HOME"/catkin_ws/src/happymimi_voice/config/dataset"
FILE=$DIR"/stanford-tagger-4.2.0.zip" 
MG_FILE=$DIR"/crawl-300d-2M.magnitude"
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
if [ ! -d $MG_FILE]; then
    echo "install crawl-300d-2M.magnitude"
    wget -c http://magnitude.plasticity.ai/fasttext/heavy/crawl-300d-2M.magnitude
    if [ ! -d $DIR ]; then
        echo -e "\e[31m ~/catkin_ws/src/happymimi_voice/dataset is not find, p      lease clone happymimi_voice \e[m"
  　else
        mv crawl-300d-2M.magnitude ../config/dataset/
    fi
fi

python nltk_download.py
python gensim_download.py

