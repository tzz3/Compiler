import re

# expression = ['S->E', 'E->aA|bB', 'A->cA|d', 'B->cB|d']
# expression = ['E->aA|bB', 'A->cA|d', 'B->cB|d']  # 应处理文法
# expression = ['E->E+T|T', 'T->T*F|F', 'F->(E)|i']

# E->aA|bB A->cA|d B->cB|d
expression = []
express = []  # 处理后表达式 切割处理
no_terminal = []  # 非终结符
terminal = []  # 终结符
symbol = ['+', '*', '(', ')']  # 符号
project = []  # 项目
projects = []  # 处理后项目
iterms = []  # 项目集规范族
inputstr = []  # 分析表输入串 list


def inputep():
    global expression
    s = input("文法：\n")
    expression = s.split()
    # print(expression)


def getterminal():
    global expression
    global no_terminal
    for e in expression:
        no_terminal.append(e[0])

    for e in expression:
        for k in e:
            if not k.isupper() and k != '-' and k != '>' and k != '|' and k not in terminal:
                terminal.append(k)
    terminal.append('#')

    print('no_terminal:', no_terminal)
    print('terminal:', terminal, end="\n\n")


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
    express.insert(0, 'S->' + express[0][0])
    print("\nexpress:", express, end="\n\n")


def init():  # 表达式处理
    global expression
    global express
    expression = []
    for i in range(len(express)):
        s = re.split(r"(->)|\|", express[i])
        for k in s:
            if k == None or k == '->' or k == '':
                s.remove(k)
        expression.append(s)
    print("expression:", expression, end="\n\n")


def addpoint():  # 项目加点
    global project
    global express
    global expression

    for e in expression:
        for i in range(len(e[1]) + 1):
            s = e[1][:i] + '·' + e[1][i:]
            project.append(e[0] + '->' + s)

    print("project:", project, end="\n\n")


def projectSplit():  # 项目切割处理
    global project
    global projects
    for i in range(len(project)):
        s = re.split(r"(->)|\|", project[i])
        for k in s:
            if k == None or k == '->' or k == '':
                s.remove(k)
        projects.append(s)
    print("projects:", projects, end="\n\n")


def Closure(I):
    """
    计算项目集I的闭包
    :param I: project
    :return: list closure计算结果
    """
    index = project.index(I)
    clist = [I]
    r = projects[index][1]
    nt = ''
    if I[-1] == '·':
        return True
    for i in range(len(r)):
        if r[i] == '·' and i < len(r) - 1:
            nt = r[i + 1]
            break

    for p in project:
        index = project.index(p)
        if p[0] == nt and projects[index][1][0] == '·':
            clist.append(p)

    return clist


def GO(I, X):
    """
    状态转移函数
    :param I: 项目集I
    :param X: 转移状态
    :return: list 结果集
    """
    j = []
    glist = []
    # 寻找a·Xb
    for i in I:
        index = i.index('·')  # index从0开始计数
        if index == len(i) - 1:  # 终结符 GO 结束
            return True
        if index > 0 and i[index + 1] == X:
            j.append(i)
            for p in project:
                if p[:index] == i[:index] and p[index + 2:] == i[index + 2:] and p[index] == i[index + 1] and p[
                    index + 1] == i[index]:
                    glist.append(p)
    return glist


def cirproject():  # 项目集规范族计算
    global projects
    global iterms
    global contact
    iterm = []  # 项目集1
    cired = []  # 已计算
    contact = []  # 联系图

    I = project[0]
    iterm.append(I)

    flag = True
    while flag == True:
        flag = False
        for i in iterm:
            if i not in cired:
                flag = True
                # 计算closure
                closure = Closure(i)
                cired.append(i)
                if closure != True:  # 终结符
                    # 计算go
                    for c in closure:
                        k = c.index('·') + 1
                        go = GO(closure, c[k])
                        if go != True:
                            for g in go:
                                ct = [closure[0], c[k], g]
                                contact.append(ct)  # 添加联系图 begin,x,end
                                if g not in iterm:
                                    iterm.append(g)

                    continue
    print("iterm:", iterm, end="\n\n")

    for i in iterm:  # 推导族内元素
        c = Closure(i)
        if c == True:
            iterms.append([i])
        else:
            iterms.append(c)
    print('iterms:', iterms, end="\n\n")

    for c in contact:  # 转换关系图
        for i in iterms:
            if c[0] in i:
                c[0] = iterms.index(i)
            if c[2] in i:
                c[2] = iterms.index(i)
    print("contact:", contact, end="\n\n")


def analysisSheet():  # 计算分析表
    global iterms
    global contact
    global table
    global action
    global goto
    table = {}
    action = {}
    goto = {}

    for c in contact:
        key = (c[0], c[1])
        if c[1].isupper():
            goto[key] = c[2]
        else:
            action[key] = 'S' + str(c[2])

    for index in range(len(iterms)):
        for iterm in iterms[index]:
            if iterm[-1] == '·' and iterm[-2] != no_terminal[0]:
                j = express.index(iterm[:-1])
                for t in terminal:
                    action[(index, t)] = 'r' + str(j)
        if iterms[index][0][-2:] == no_terminal[0] + '·':
            action[(index, '#')] = 'acc'

    tab = '\t' * 2
    print('----' * (len(terminal + no_terminal) + 1) * 2)
    print(tab * 2, 'action', tab * 4, 'goto')
    print('状态', end=tab)
    for t in terminal:
        print(t, end=tab)
    print('|', end=tab)
    for n in no_terminal:
        print(n, end=tab)
    print('\n', '----' * (len(terminal + no_terminal) + 1) * 2)
    for i in range(len(iterms)):
        print(i, end=tab)
        for t in terminal:
            flag = False
            for key in action:
                if key == (i, t):
                    flag = True
                    print(action[key], end=tab)
                    break
            if flag == False:
                print(end=tab)
        print('|', end=tab)
        for n in no_terminal:
            flag = False
            for key in goto:
                if key == (i, n):
                    flag = True
                    print(goto[key], end=tab)
            if flag == False:
                print(end=tab)
        print()
    print('----' * (len(terminal + no_terminal) + 1) * 2)

    print(action)
    print(goto)


def inputastr():  # 输入串
    global inputstr
    global s
    if len(s) == 0:
        s = input("输入串:")  # i+i*i
    # str = re.split(r'([+*#])', s)
    # str = s.split()
    str = s
    print(str)
    for m in range(len(str) - 1, -1, -1):
        inputstr.append(str[m])


def analyse():
    global action
    global goto
    global analysisform
    global inputstr
    analysisform = []

    states = [0]
    symbol = ['#']
    ex = ""
    inputstr.insert(0, '#')
    print(inputstr)
    info = '0和#进栈'
    # print(inputstr.pop(), inputstr)
    # exit(0)
    row = [states, symbol, ex, inputstr, info]
    print(row)
    analysisform.append(row)

    while True:
        ex = ""
        info = ''
        stop = states[-1]
        symtop = symbol[-1]
        itop = inputstr[-1]

        key = (stop, itop)
        if action.__contains__(key):
            value = action[key]
            if value == 'acc':
                break

            state = int(value[-1])
            if value[0] == 'S':  # 移进
                info = inputstr[-1] + '和S' + str(state) + '进栈'
                states.append(state)
                symbol.append(inputstr.pop())
            elif value[0] == 'r':
                # 状态和符号退栈 表达式头和状态入栈
                ex = express[state]
                ne = ex[0]
                re = ex[(ex.index('>') + 1):]
                length = len(ex.split('>')[-1])
                s1 = ""
                s2 = ""
                for l in range(length):
                    s1 += str(states.pop()) + ' '
                    s2 += symbol.pop() + ' '

                symbol.append(ne)
                v = goto[(states[-1], ne)]
                states.append(v)

                info = s1 + '和 ' + s2 + '退栈, ' + ne + '和S' + str(state) + '进栈'
            row = [states, symbol, ex, inputstr, info]
            print(row)
            analysisform.append(row)


if __name__ == '__main__':
    # E->aA|bB A->cA|d B->cB|d
    #
    # expression = []
    # expression = ['E->aA|bB', 'A->cA|d', 'B->cB|d']  # 应处理文法
    expression = ['E->E+T|T', 'T->T*F|F', 'F->(E)|i']
    s = 'i+i*i'
    # s = 'ad'

    # inputep()  # 输入文法
    getterminal()
    expressSplit()
    init()

    addpoint()  # 项目加点
    projectSplit()  # 项目切割

    cirproject()  # 计算项目集规范族
    analysisSheet()  # 计算预测分析表

    inputastr()  # 输入分析输入串
    analyse()  # LR分析过程
