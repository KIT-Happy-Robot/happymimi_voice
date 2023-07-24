#! /bin/bash
sudo -E apt install portaudio19-dev
pip install git+https://github.com/openai/whisper.git
pip install -r requirements.txt
DIR="../config/dataset"
FILE=$DIR"/stanford-postagger" 
MG_FILE=$DIR"/crawl-300d-2M.magnitude"
echo $DIR
if [ ! -e $FILE ]; then
  echo "install stanford data"
  wget https://nlp.stanford.edu/software/stanford-tagger-4.2.0.zip
  unzip stanford-tagger-4.2.0.zip
  mv stanford-postagger-full-2020-11-17 ../config/dataset/stanford-postagger
fi

python3 -m spacy download en_core_web_trf
python3 nltk_download.py
