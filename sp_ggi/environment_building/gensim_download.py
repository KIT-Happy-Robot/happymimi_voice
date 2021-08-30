import gensim.downloader as api
model=api.load("glove-twitter-200")
'''
while(1):
    print("please input")
    str=input()
    if str=="f":
        break
    else:
        print(model.most_similar(str))
'''
