# sp_ggi
## set_up

このパッケージではgensimとnltkを用いており、それぞれ追加データのダウンロードが必要
- 必要ライブラリ・モジュールのインストール
```
#仮想環境の作成を推奨(python3.3以降Virtualenv)
~sp_ggi$python3.8 -m venv env
~sp_ggi$source env/bin/activate
~sp_ggi$cd encironment_building
~sp_ggi/encironment_building$pip install -r requirements.txt
~sp_ggi/encironment_building$deactivate
```
- nltkとgensimの環境構築
```
~sp_ggi/encironment_building$. nltk_gensim_enviroment.bash
```
### ggi_trainingのアルゴリズム  
特徴と名前をオブジェクトと場所に分けて登録。特徴と名前の識別に関しては、nltkというモジュールを使用し、品詞分解を行うことで識別している。  
それぞれのデータの保存方法に関しては、辞書型で場所の特徴と名前、オブジェクトの特徴と名前の4つに分け、pickleファイルとして保存している。  

### test_phaseのアルゴリズム
品詞分解によって場所とオブジェクトの情報に別け、さらに特徴と名前に分解、リストに追加する  
ggi_learningで作ったpickleファイルとword2vecの学習済みデータを呼び出し、優先度の高い順に条件を確認していく。  優先順位は以下の通りである。
#### 優先順位
- オブジェクトの名前と場所の名前が一致している
- 場所の名前と特徴が一致している
- 場所の名前がコサイン類似度で一定の数値を満たしていて、特徴が一致している
- オブジェクトの名前と特徴が一致している
- 場所の名前がコサイン類似度で一定の数値を満たしている。
- オブジェクトの名前がコサイン類似度で一定の数値を満たしている
### word2vecの学習済みモデル
https://github.com/RaRe-Technologies/gensim-data
glove-wiki-gigaword-100

### nltkのtagger
stanford大学のものを利用
https://nlp.stanford.edu/software/stanford-tagger-4.2.0.zip


