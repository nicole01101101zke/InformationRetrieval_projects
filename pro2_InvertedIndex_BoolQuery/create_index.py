import os

#存放数据集的文件路径
path1 = "D:\\大四上\\信息检索\\pro02\\data\\数据"
path2 = "D:/大四上/信息检索/pro02/data/数据/"
filenames = os.listdir(path1)
dic = {}
count = {}

#对每一个txt文件
for name in filenames:
    docID = name.split('.')[0] #取出.txt前面的部分，记录为docID
    with open(path2 + name, "r") as f: # 打开文件
        text = f.read().lower() #按要求把单词都转成小写
        words = text.split() #直接用空格作为分隔符
    f.close()
    for word in words: #用字典dic存{word,docID}键值对
        if word in dic:
            dic[word].append(docID)
        else:
            dic[word] = [docID]

for temp in dic:
    dic[temp] = list(set(dic[temp]))
    count[temp] = len(dic[temp])
    dic[temp].sort()

table0 = sorted(count.items(), key=lambda obj:obj[1])
table0.reverse()

#把出现次数前100的排名去掉
print("排名前100的单词：\n")
k=0
for c in table0:
    if k >= 100:
       break
    else:
        print(c[0]+"\n")
        dic.pop(c[0])
        count.pop(c[0])
    k=k+1

table1 = sorted(dic.items(), key=lambda obj:obj[0])
table2 = sorted(count.items(), key=lambda obj:obj[0])

dic_sorted = dict(table1)
count_sorted = dict(table2)


with open("./dict.index.txt", "w") as f:  # 打开文件
    for word in dic_sorted:
        f.write(str(word) + '\t' + str(count_sorted[word]) + '\t' + ' '.join(dic_sorted[word]) + '\n')
f.close()