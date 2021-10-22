#! /bin/bash
sudo -E apt install portaudio19-dev
pip install -r requirements.txt
DIR=$HOME"/catkin_ws/src/happymimi_voice/config/dataset"
FILE=$DIR"/stanford-postagger" 
MG_FILE=$DIR"/crawl-300d-2M.magnitude"
echo $DIR
if [ ! -e $FILE ]; then
  echo "install stanford data"
  wget https://nlp.stanford.edu/software/stanford-tagger-4.2.0.zip
  unzip stanford-tagger-4.2.0.zip
  mv stanford-postagger-full-2020-11-17 ../config/dataset/stanford-postagger
fi
if [ ! -e $MG_FILE]; then
    echo "install crawl-300d-2M.magnitude"
    wget -c http://magnitude.plasticity.ai/fasttext/heavy/crawl-300d-2M.magnitude
    mv crawl-300d-2M.magnitude ../config/dataset/
fi

python nltk_download.py
python gensim_download.py

