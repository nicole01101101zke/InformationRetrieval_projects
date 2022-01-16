import os
import re
import nltk
import math


class Prepare:

    def __init__(self, Main_Path):
        self.Main_Path = Main_Path
        self.Dic_Path = Main_Path + "_dic"
        self.Count_Path = Main_Path + "_count"
        self.news_group = {}

    # 为每个文件创建词典
    def create_dic(self):
        # 判断是否已创建完毕
        if not os.path.exists(self.Dic_Path):
            print("start create " + self.Dic_Path)
            os.makedirs(self.Dic_Path)
        else:
            print("{} already exists".format(self.Dic_Path))
            print()
            return None
        nltk.download('stopwords')
        for group_name in os.listdir(self.Main_Path):  # 遍历每一个文件夹
            group_path = self.Main_Path + '/' + group_name
            group_path_dic = self.Dic_Path + '/' + group_name
            if not os.path.exists(group_path_dic):
                os.makedirs(group_path_dic)
            for file_name in os.listdir(group_path):  # 遍历每一类下的每一个文件
                file_path = group_path + '/' + file_name  # 原文件路径
                file_path_dic = group_path_dic + '/' + group_name + "-" + file_name  # 字典文件路径
                fw = open(file_path_dic, 'w')
                content = open(file_path, 'r', encoding='utf-8', errors='ignore').readlines()  # 读取原文件的全部内容
                for line in content:
                    word_list = get_words(line)  # 该函数返回去除停用词后一个句子的单词列表
                    for word in word_list:
                        fw.write('{}\n'.format(word))
                fw.close()
            print(group_name + "词典文件创建成功")
        print(self.Dic_Path + "下的文件全部创建成功")
        print()
        return None

    # 统计词频
    def count_tokens(self):
        if not os.path.exists(self.Count_Path):
            print("start create {}".format(self.Count_Path))
            os.makedirs(self.Count_Path)
        else:
            print("{} already exists".format(self.Count_Path))
            print()
            return None
        for group_name in os.listdir(self.Dic_Path): # 计算每个文件的词频并写入文件系统
            group_path_dic = self.Dic_Path + '/' + group_name
            group_path_count = self.Count_Path + '/' + group_name
            if not os.path.exists(group_path_count):
                os.makedirs(group_path_count)
            for file in os.listdir(group_path_dic):
                word_dic = {}
                file_path_dic = group_path_dic + '/' + file
                file_path_count = group_path_count + '/' + file
                for line in open(file_path_dic).readlines():
                    word = line.strip('\n')
                    if word in word_dic:
                        word_dic[word] += 1
                    else:
                        word_dic[word] = 1
                f = open(file_path_count, 'w')
                for word in word_dic:
                    f.write('{} {}\n'.format(word, word_dic[word]))
                f.close()
            print(group_name + "统计词频成功")
        print(self.Count_Path + "下的文件全部创建成功")
        return None

    # 得到文档集结构信息
    def create_news_group(self):
        for group_name in os.listdir(self.Count_Path):
            self.news_group[group_name] = []
            group_path = self.Count_Path + '/' + group_name
            for file_name in os.listdir(group_path):
                self.news_group[group_name].append(file_name)
        return None


class NaiveBayes:

    def __init__(self, Count_Path):
        self.train_set = {}
        self.test_set = {}
        self.NB_word_P = {}
        self.NB_group_p = {}
        self.Count_Path = Count_Path
        self.total_word = {}

    def nb_multinomial_train(self, train_set):
        self.train_set = train_set
        for group in self.train_set:
            group_path_count = self.Count_Path + '/' + group
            self.NB_word_P[group] = {}
            for file in self.train_set[group]:
                file_path_count = group_path_count + '/' + file
                word_count = {}
                with open(file_path_count, 'r', encoding='utf-8', errors='ignore') as f:
                    while 1:
                        line = f.readline().split()
                        if not line:
                            break
                        if line[0] not in word_count:
                            word_count[line[0]] = int(line[1])
                        else:
                            word_count[line[0]] += int(line[1])
                for word in word_count:
                    if word not in self.NB_word_P[group]:
                        self.NB_word_P[group][word] = word_count[word]
                    else:
                        self.NB_word_P[group][word] += word_count[word]
                    if word not in self.total_word:
                        self.total_word[word] = word_count[word]
                    else:
                        self.total_word[word] += word_count[word]

        group_total = {}
        total = sum(self.total_word.values())
        for group in self.NB_word_P:
            group_total[group] = 0
            for word in self.total_word:
                if word not in self.NB_word_P[group]:
                    self.NB_word_P[group][word] = 0
                group_total[group] += self.NB_word_P[group][word]
            print("Group {} counts of words are {}".format(group, group_total[group]))
            self.NB_group_p[group] = math.log(float(group_total[group]) / total)
        print("counts of words in total training set is {}".format(total))
        print()
        for i in self.NB_word_P:
            for word in self.NB_word_P[i]:
                self.NB_word_P[i][word] = math.log(
                    float(self.NB_word_P[i][word] + 0.01) / (group_total[i] + 0.01 * len(self.NB_word_P[i])))
        return None

    def nb_multinomial_test(self, test_set):
        self.test_set = test_set
        test_news = {}
        for group in self.test_set:
            group_index_path = 'test_count/' + group
            for news in self.test_set[group]:
                test_news[news] = {}
                news_index_path = group_index_path + '/' + news
                with open(news_index_path, 'r', encoding='utf-8', errors='ignore') as f:
                    while 1:
                        line = f.readline().split()
                        if not line:
                            break
                        test_news[news][line[0]] = int(line[1])

        fw = open("D:/大四上/信息检索/pro04/TextClassification/c_10182100208.txt", 'w')
        for news in test_news:
            largest_p = float("-inf")
            prediction = ""
            for group in self.NB_word_P:
                p = self.NB_group_p[group]
                for word in self.NB_word_P[group]:
                    if word in test_news[news]:
                        p = p + (self.NB_word_P[group][word] * test_news[news][word])
                if p > largest_p:
                    prediction = group
                    largest_p = p
            names = news.split("-")
            name = names[len(names) - 1]
            fw.write(name + ":" + prediction + "\n")
        fw.close()
        return None


def get_words(line):
    ps = nltk.PorterStemmer()
    sp = re.compile('[^a-zA-Z]')
    st = nltk.corpus.stopwords.words('english')
    words = [ps.stem(word.lower()) for word in sp.split(line) if len(word) > 0 and word.lower() not in st]
    return words
