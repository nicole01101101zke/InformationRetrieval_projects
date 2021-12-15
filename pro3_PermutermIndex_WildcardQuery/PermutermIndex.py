import os

tokens = {}
count = {}
path = r"D:\大四上\信息检索\pro02\data\数据"
path2 = "D:/大四上/信息检索/pro02/data/数据/"

for root, dirs, files in os.walk(path):
    for name in files:
        docID = name.split('.')[0]  # 取出.txt前面的部分，记录为docID
        with open(path2 + name, "r") as f:  # 打开文件
            text = f.read().lower()  # 按要求把单词都转成小写
            words = text.split()  # 直接用空格作为分隔符
        f.close()
        for word in words:  # 用字典tokens存{word,docID}键值对
            if word in tokens:
                tokens[word].append(docID)
            else:
                tokens[word] = [docID]

for temp in tokens:
    tokens[temp] = list(set(tokens[temp]))
    count[temp] = len(tokens[temp])
    tokens[temp].sort()

table0 = sorted(count.items(), key=lambda obj:obj[1])
table0.reverse()

#把出现次数前100的排名去掉
k = 0
for c in table0:
    if k >= 100:
       break
    else:
        #print(c[0]+"\n")
        tokens.pop(c[0])
        count.pop(c[0])
    k += 1

def rotate(str, n):
    return str[n:] + str[:n]

file = open("D:\大四上\信息检索\pro03\WildcardQuery\PermutermIndex.txt","w")
keys = tokens.keys()
for key in sorted(keys):
    dkey = key + "$"
    for i in range(len(dkey),0,-1):
        out = rotate(dkey,i)
        file.write(out)
        file.write(" ")
        file.write(key)
        file.write("\n")
file.close()