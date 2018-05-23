import copy
import re

# expression = []
# E->TA A->+TA|# T->FB B->*FB|# F->(E)|i
expression = ['E->TA', 'A->+TA|#', 'T->FB', 'B->*FB|#', 'F->(E)|i']
express = []
no_terminal = []
terminal = []
symbol = ['+', '*', '(', ')']
first = {}
follow = {}
forecastform = {}


def inputExpression():  # 表达式输入
    global expression
    s = input("文法：\n")
    expression = s.split()
    # print(expression)


def getterminal():
    global expression
    global terminal
    for e in expression:
        no_terminal.append(e[0])
    for e in expression:
        for k in e:
            if k not in terminal and not k.isupper() and k != '-' and k != '>' and k != '|':
                terminal.append(k)
    # print(terminal)
    terminal = list(set(terminal))


def expressSplit():  # 文法改写
    global expression
    global express
    for e in expression:
        # print(e)
        s = re.split(r"(->)|\|", e)
        for k in s:
            if k == None or k == '->' or k == '':
                s.remove(k)
        for k in s[1:]:
            express.append(s[0] + '->' + k)
        # print(s)
    # print("\nexpress:", express, end="\n\n")
    print('\n  改写：')
    for e in range(len(express)):
        print('  ', e, '  ', express[e])
    print()


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
    # print("expression:", expression, end="\n\n")


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
    while flag:
        flag = False
        for key in first:
            fList = first.get(key)
            for f in fList:
                if f.isupper():
                    fList.remove(f)
                    for g in first.get(f):
                        if g != '#':
                            fList.append(g)
                    # fList += first.get(f)
                    flag = True


"""FOLLOW"""


def infer(x):
    for f in first:
        if x == f:
            for k in first[f]:
                if k == '#':
                    return True
    return False


def cirFollow():
    global follow
    follow[no_terminal[0]] = ['#']  # 规则 1

    for t in no_terminal:
        addlist = []
        for e in expression:
            for w in range(len(e[1])):
                if w == len(e[1]) - 1:
                    if e[1][w] == t:
                        addlist.append(e[0])  # 规则 4
                else:
                    if e[1][w] == t:
                        x = e[1][w + 1]
                        if x.isupper():  # 非终结符
                            for f in first[x]:  # 规则 3
                                if f != '#':
                                    addlist.append(f)

                            # 判断是否为空
                            if infer(x):  # 推导出 '#'   后面所有都为空
                                addlist.append(e[0])  # 规则 4
                        else:
                            addlist.append(x)  # 规则2

        addlist = list(set(addlist))  # 去重
        if follow.__contains__(t):
            follow[t] += addlist
        else:
            follow[t] = addlist

    flag = True
    while flag:  # 判断是否计算完成
        flag = False
        for f in follow:
            value = follow.get(f)
            for v in value:
                if v.isupper():
                    if v == f:
                        value.remove(v)
                    else:
                        value.remove(v)
                        for k in follow.get(v):
                            if k not in value:
                                value.append(k)
                                flag = True


"""LL1"""


def isLL1():
    if leftRecursion():
        if recall():
            cirFirst()
            cirFirst2()

            cirFollow()
            outputf()

            # LL1 规则2
            for e in express:
                for k in express:
                    if e != k and e[0] == k[0] and first[e] == first[k]:
                        print("首终结符集 相交")
                        return False

            # LL1 3
            for n in no_terminal:
                if '#' in first[n]:
                    for k in first[n]:
                        if k in follow[n] and k != '#':
                            print("LL1 规则3 不符合")
                            return False
            return True
        else:
            print("包含回溯")
            return False
    else:
        print("包含左递归")
        return False


"""预测分析表"""


def forecast():
    global forecastform

    for k in range(len(expression)):
        t = expression[k][0]
        e = express[k]
        for n in first[e]:  # 规则2
            if not n.isupper():
                key = (t, n)
                forecastform[key] = express[k]
        if '#' in first[e]:  # 规则3
            for f in follow[t]:
                forecastform[(t, f)] = express[k]

            if '#' in follow[t]:
                forecastform[(t, '#')] = express[k]

    # E->TA A->+TA|# T->FB B->*FB|# F->(E)|i
    tab = '\t' * 3
    print('\t' * (len(terminal)), '预测分析表')
    print('----' * (len(terminal) + 2) * 2)
    print('%-10s' % (' '), end='')
    for t in terminal:
        print('%-10s' % (t), end='')
    print()
    print('----' * (len(terminal) + 2) * 2)
    for n in no_terminal:
        print('%3s' % (n), end=' ' * 5)
        row = []
        for t in terminal:
            key = (n, t)
            if key in forecastform:
                print('%-10s' % (forecastform[key]), end='')
                row.append(forecastform[key])
            else:
                print('%-10s' % (''), end='')
                row.append('')
        print()
    print('----' * (len(terminal) + 2) * 2, end='\n' * 2)


"""递归下降分析"""


def analyse():
    global s
    global forecastform
    analyseform = []

    str = s
    sp = re.split(r'([+*#])', s)
    s = []
    for k in sp:
        if k != None and k != '':
            s.append(k)

    stringstack = []
    for m in range(len(s) - 1, -1, -1):
        stringstack.append(s[m])
    # print(stringstack)
    tops = len(stringstack)

    alastack = ['#', no_terminal[0]]
    # print(alastack)
    topa = len(alastack)

    print("\n对符号串", str[:-1], "的分析过程", end='\n\n')
    while alastack[-1] != '#':
        X = alastack[-1]  # 栈顶符号
        a = stringstack[-1]  # 输入符号
        info = ''
        if X == a:
            if X == '#':  # 分析成功
                info = "接受"
            else:  # 获得一次匹配
                alastack.remove(X)
                info = stringstack[-1] + '匹配'
                stringstack = stringstack[:-1]
        else:
            key = (X, a)
            if forecastform.__contains__(key):
                alastack.remove(X)  # 出栈
                evalue = forecastform[key]  # 产生式
                info = evalue
                value = evalue.split('>')[1]
                for v in range(len(value) - 1, -1, -1):  # 反序压栈
                    if value[v] != '#':
                        alastack.append(value[v])
                if alastack[-1] == '#':
                    info = "接受"
        af = [copy.copy(alastack), stringstack, info]  # 使用copy来复制内容，否则会随alastack地址内容的改变而改变
        analyseform.append(af)

    length = len(analyseform)
    print('%-5s %-11s %-10s %s' % ('序号', '状态栈', '符号栈', '推导所用产生式或匹配'))
    for index in range(length):
        af = analyseform[index]
        a = ''.join(af[0])
        symbol = ''.join(af[1])
        info = af[2]
        print('%-7d %-13s %-13s %s' % (index, a, symbol, info))


def outputf():
    global opf
    if opf == True:
        print("FIRST:", )
        for f in first:
            print('First(', f, ') = ', first[f])

        print("\nFOLLOW:")
        for f in follow:
            print('Follow(', f, ') = ', follow[f])


if __name__ == '__main__':
    inputExpression()  # E->TA A->+TA|# T->FB B->*FB|# F->(E)|i

    # 表达式处理
    getterminal()
    # print("no_terminal:", no_terminal)
    # print("terminal:", terminal, end="\n\n")

    expressSplit()
    init()
    # 表达式正确性验证
    if not check():
        print("表达式错误")
        exit(0)
    # s = 'i+i*i#'  # 分析符号串

    opf = False  # first follow 输出
    if isLL1():
        forecast()
        s = input("分析符号串：")  # i+i*i
        s += '#'
        analyse()
