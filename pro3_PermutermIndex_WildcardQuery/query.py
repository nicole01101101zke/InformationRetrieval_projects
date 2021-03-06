from BTrees.OOBTree import OOBTree

dict_inverted = open("./dict.index.txt", 'r')
dict_permuterm = open("./PermutermIndex.txt", 'r')
terms1 = dict_inverted.readlines()
terms2 = dict_permuterm.readlines()
inverted = {}
permuterm = {}


for term in terms1:
    term_s = term.split()
    #count[term_s[0]] = term_s[1]
    for i in range(int(term_s[1])):
        if term_s[0] in inverted:
            inverted[term_s[0]].append(int(term_s[2+i]))
        else:
            inverted[term_s[0]] = [(int(term_s[2+i]))]

for term in terms2:
    term_s = term.split()
    permuterm[term_s[0]] = term_s[1]

t1 = OOBTree(permuterm)
t2 = OOBTree(inverted)

def WildCardQuery(paras, case):

    if case == 1:
        query = paras[0] + "$"
        processQuery(query, False)
    elif case == 2:
        query = "$" + paras[0]
        processQuery(query, True)
    elif case == 3:
        query = paras[1] + "$"
        processQuery(query, True)
    elif case == 4:
        query = paras[1]
        processQuery(query, True)
    else:
        query = paras[1] + "$" + paras[0]
        processQuery(query, True)



def processQuery(query, flag):
    #temp_count = {}
    term_list = []
    for tk in t1.keys():
        if flag == True:
            #print(1)
            if tk.startswith(query):

                term_list.append(t1[tk])
                #temp_count[permuterm[tk]] = int(count[permuterm[tk]])
        else:
            if tk == query:
                term_list.append(t1[tk])
                #temp_count[permuterm[tk]] = int(count[permuterm[tk]])
    #table = sorted(temp_count.items(), key=lambda x: x[1], reverse=True)
    #temp_count_sorted = dict(table)

    #print(' '.join(str(i) for i in temp_count_sorted))
    #print(' '.join(str(temp_count_sorted[i]) for i in temp_count_sorted))
    print(' '.join(str(i) for i in term_list))

    docID = []
    i=0
    for term in term_list:
        if i == 0 or i == 1:
            docID.append(t2[term])
        i += 1

    if len(docID) == 0:
        print("?????????????????????...")
        return
    if len(docID) >= 2:
        result = list(set(docID[0]).union(set(docID[1])))
    else:
        result = list(set(docID[0]))
    result.sort()
    print(' '.join(str(i) for i in result))
    # print(temp)

    return


if __name__ == '__main__':
    query = input("?????????????????????????????????")
    while query != "exit":
        parts = query.split("*")
        if '*' not in query:
            print("?????????????????????????????????*?????????????????????...")
            WildCardQuery(parts, 1)
        elif len(parts) == 3 and parts[0] == '' and parts[2] == '':
            WildCardQuery(parts, 4)
        elif len(parts) > 2:
            print("???????????????????????????????????????????????????????????????????????????*")
        else:
            if parts[0] == '' and parts[1] != '':
                WildCardQuery(parts, 3)
            elif parts[0] != '' and parts[1] == '':
                WildCardQuery(parts, 2)
            elif parts[0] != '' and parts[1] != '':
                WildCardQuery(parts, 5)
            else:
                print("??????????????????*????????????")

        query = input("??????????????????????????????")
    print("???????????????")