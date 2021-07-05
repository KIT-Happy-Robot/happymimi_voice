source ../../env/bin/activate
wget https://nlp.stanford.edu/software/stanford-tagger-4.2.0.zip
unzip stanford-tagger-4.2.0.zip
mv stanford-postagger-full-2020-11-17 ~/catkin_ws/src/happymimi_common/config/stanford-postagger
python nltk_download.py
python gensim_download.py
