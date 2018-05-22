import re

# expression = ['S->E', 'E->aA|bB', 'A->cA|d', 'B->cB|d']
expression = ['E->aA|bB', 'A->cA|d', 'B->cB|d']  # 应处理文法
express = []  # 处理后表达式 切割处理
no_terminal = []  # 非终结符
terminal = []  # 终结符
symbol = ['+', '*', '(', ')']  # 符号
project = []  # 项目
projects = []  # 处理后项目
iterm = []  # 项目集规范族


def input():
    global expression
    s = input("文法：\n")
    expression = s.split()
    print(expression)


def getterminal():
    global expression
    global no_terminal
    for e in expression:
        no_terminal.append(e[0])

    for e in expression:
        for k in e:
            if not k.isupper() and k != '-' and k != '>' and k != '|' and k not in terminal:
                terminal.append(k)

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
    # print(I, X)

    j = []
    glist = []
    # 寻找a·Xb
    for i in I:
        index = i.index('·')  # index从0开始计数
        if index > 0 and i[index + 1] == X:
            j.append(i)
            for p in project:
                if p[:index] == i[:index] and p[index + 2:] == i[index + 2:] and p[index] == i[index + 1] and p[
                    index + 1] == i[index]:
                    glist.append(p)
    return glist


def cirproject():  # 项目集规范族计算
    global projects

    # for p in projects:
    I = project[0]
    closure = Closure(I)
    print("closure:", closure)

    for i in closure:
        k = i.index('·') + 1
        go = GO(closure, i[k])
        print("go:", go)


if __name__ == '__main__':
    getterminal()
    expressSplit()
    init()

    addpoint()
    projectSplit()

    cirproject()
