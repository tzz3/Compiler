import re

# expression = []
expression = ['E->TX', 'X->+TX|#', 'T->FY', 'Y->*FY|#', 'F->(E)|i']
express = []
symbol = ['+', '*', '(', ')']
first = {}


def inputExpression():  # 表达式输入
    global expression
    s = input("文法：\n")
    expression = s.split()
    print(expression)


def expressSplit():  # 文法改写
    global expression
    global express
    for e in expression:
        print(e)
        s = re.split(r"(->)|\|", e)
        for k in s:
            if k == None or k == '->' or k == '':
                s.remove(k)
        for k in s[1:]:
            express.append(s[0] + '->' + k)
        # print(s)
    print("\nexpress:", express, end="\n\n")


def init():  # 表达式处理
    global expression
    global express
    expression = []
    for i in range(len(express)):
        # print(expression[i])
        s = re.split(r"(->)|\|", express[i])
        for k in s:
            if k == None or k == '->' or k == '':
                s.remove(k)
        # print(s)
        expression.append(s)
    print("expression:", expression, end="\n\n")


def check():  # 表达式验证
    global expression
    for e in expression:
        if e[0].islower():
            return False
    return True


def leftRecursion():  # 判断左递归
    global expression
    for e in expression:
        for k in e[1:]:
            if e[0] == k:
                return False
    return True


def recall():  # 判断回溯
    global expression
    for e in expression:
        s = []
        for k in e[1:]:
            if k[0] in s:
                return False
            else:
                s.append(k[0])
    return True


"""FIRST"""


def infer_(k):  # 能否推导出#
    global expression
    for e in expression:
        if e[0] == k:
            for k in e[1:]:
                if k == '#':
                    return True
    return False


def First(e):
    global first
    add = []
    for w in e[1:]:  # e-此条expression
        # 终结符和空字符
        if w[0].islower() or (w[0] == '#' and len(w) == 1) or w[0] in symbol:
            add.append(w[0])
        # 非终结符
        elif w[0].isupper():
            if infer_(w[0]):
                for m in w[1:]:
                    if not infer_(m):
                        add.append(m)
                        continue
                add.append('#')
            else:
                add.append(w[0])
    # print(add)
    return add


def cirFirst():  # 第一次计算
    for e in expression:
        addList = First(e)

        key = e[0]
        getKey = first.get(key)
        if getKey == None:
            first[key] = addList
        else:
            for add in addList:
                if add not in getKey:
                    getKey.append(add)
            first[key] = getKey

    for m in range(len(express)):
        e = expression[m]
        addList = First(e)

        key = express[m]
        getKey = first.get(key)
        if getKey == None:
            first[key] = addList
        else:
            for add in addList:
                if add not in getKey:
                    getKey.append(add)
            first[key] = getKey


def cirFirst2():
    flag = True
    while flag == True:
        flag = False
        for key in first:
            fList = first.get(key)
            for f in fList:
                if f.isupper():
                    fList.remove(f)
                    fList += first.get(f)
                    flag = True


def getFollow():
    pass


def isLL1():
    pass


if __name__ == '__main__':
    # inputExpression()

    # 表达式处理
    expressSplit()
    init()
    # 表达式正确性验证
    if not check():
        print("表达式错误")
        exit(0)

    if leftRecursion():
        if recall():
            cirFirst()
            cirFirst2()
            print("FIRST:", )
            for f in first:
                print('First(', f, ') = ', first[f])
        else:
            print("包含回溯")
    else:
        print("包含左递归")

    pass
