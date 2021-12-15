dict_index = open("./dict.index.txt", 'r')
terms = dict_index.readlines()
dic = {}

for term in terms:
    term_s = term.split()
    for i in range(int(term_s[1])):
        if term_s[0] in dic:
            dic[term_s[0]].append(int(term_s[2+i]))
        else:
            dic[term_s[0]] = [(int(term_s[2+i]))]


def bool_query(paras, char):
    list_docID = []
    for para in paras:
        if para in dic:
            list_docID.append(dic[para])
        else:
            list_docID.append([])
    result = list_docID[0]
    if char == "and":
        result = list(set(result).intersection(set(list_docID[1])))
    elif char == 'or':
        result = list(set(result).union(set(list_docID[1])))
    elif char is None:
        result = result
    else:
        print("输入不正确，请输入一个布尔查询Q （And Or 操作）")
        return
    if not result:
        print("找不到结果...")
        return
    result.sort()
    print(' '.join(str(i) for i in result))


if __name__ == '__main__':
    query = input("您可以开始布尔查询：")
    while query != "exit":
        paras = []
        query_s = query.lower().split()
        if len(query_s) == 1:
            char = None
            paras.append(query_s[0])
            bool_query(paras, char)
        elif len(query_s) == 0:
            print("请输入内容\n")
        else:
            for i in range(0, len(query_s), 2):
                paras.append(query_s[i])
            char = query_s[1]
            bool_query(paras, char)
        query = input("可以继续布尔查询：")
    print("退出成功！")