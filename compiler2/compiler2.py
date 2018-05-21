wordCode = ['', 'program', 'var', 'integer', 'bool', 'real', 'char', 'const', 'begin', 'if', 'then', 'else', 'while',
            'do', 'for', 'to', 'end', 'read', 'write', 'true', 'false', 'not', 'and', 'or', '+', '-', '*', '/', '<',
            '>', '<=', '>=', '==', '<>', 'id', '整常数', '实常数', '字符常数', '布尔常数', '=', ';', ',', '\'', '/*', '*/', ':', '(',
            ')', '.', ':=', 'repeat', 'until']
# 1-20 关键字  21-33 运算符  34 标识符  35-38 常数  39-49 界符 50-51 repeat util
tokenList = []
symList = []
errorList = []
t = -1
token = ''
treeNum = 2

tokenPath = "../compiler1/TOKEN.txt"
with open(tokenPath, 'r') as f:
    tk = f.readlines()
    for k in tk:
        split = k.split()
        if len(split)==3:
            tokenList.append(split[1])
    tokenList = tokenList[1:]
    # print(tokenList)

symPath = '../compiler1/SYM.txt'
with open(symPath, 'r') as f:
    sym = f.readlines()
    for s in sym:
        split = s.split()
        symList.append(split)
    symList = symList[1:]
    # print(symList)


# 获取下一个token值
def getnexttoken():
    global t
    global token
    t = t + 1
    if t < len(tokenList):
        token = tokenList[t]
        return token
    else:
        token = False
        return False


def lasttoken():
    global t
    global token
    # print(tokenList)
    t = t - 1
    if t >= 0 and t < len(tokenList):
        token = tokenList[t]
        return True
    else:
        token = False
        return False


# 是否标识符 √
def isIdentifider():
    n = 0
    if token in wordCode[1:21] or token in wordCode[50:]:
        return False
    if token[n].isalpha():
        n += 1
        while n < len(token) and (token[n].isalpha() or token[n].isdigit()):
            n += 1
        if n >= len(token):
            return True
        else:
            return False
    else:
        return False


# 修改符号表
def changeSym(name, value, type):
    for sym in symList:
        if name == sym[0]:
            if type == 'value':  # 修改值
                sym[3] = value
            if type == 'type':  # 修改类型
                sym[2] = value


# 算术表达式
def ael():
    global token
    token = token.replace('.', '', 1)
    if isIdentifider() or token.isdigit():
        return True
    else:
        return False


def factor():
    if ael():
        getnexttoken()
    elif token == '-':
        getnexttoken()
        factor()
    elif token == '(':
        getnexttoken()
        aexp()
        if token == ')':
            getnexttoken()
            aexp()
    else:
        return


def term():
    factor()
    if token == '*' or token == '/':
        getnexttoken()
        term()
    else:
        return


def aexp():  # 算术表达式
    global treeNum
    print('--' * treeNum, '算术表达式处理开始')
    treeNum += 2
    if token == '+' or token == '-':
        getnexttoken()
        term()
    else:
        term()
    if token == '+' or token == '-':
        getnexttoken()
        aexp()
        treeNum -= 2
        print('--' * treeNum, '算术表达式处理结束')
    else:

        treeNum -= 2
        print('--' * treeNum, '算术表达式处理结束')

        if token == ';' or token == ')' or token in wordCode[
                                                    28:34] or token == 'do' or token == 'to' or token == 'until':
            return
        else:
            error('算术表达式错误')


# 表达式
def expression():
    if token == '(':
        getnexttoken()
        expression()
    while isIdentifider() or token.isdigit():
        getnexttoken()
        if token == ')':
            getnexttoken()
            return
        elif token == ';':
            getnexttoken()
            return
        elif token in wordCode[21:34]:
            getnexttoken()
        else:
            error('expression error')


# 逻辑表达式
def bel():
    if isIdentifider() or token == 'true' or token == 'false':
        return True
    else:
        return False


def bfactor():
    if bel():
        getnexttoken()
        if token in wordCode[24:28]:
            aexp()  # ->  >
            if token in wordCode[28:34]:
                getnexttoken()
                aexp()
        else:
            getnexttoken()
            if token in wordCode[28:34]:
                getnexttoken()
                aexp()
    elif token == 'not':
        getnexttoken()
        bfactor()
    elif token == '(':
        getnexttoken()
        bexp()
        if token != ')':
            error('() error')
    else:
        return


def bterm():
    bfactor()
    getnexttoken()
    if token == 'and':
        getnexttoken()
        bterm()
    elif token == 'then' or token == 'do':
        lasttoken()
        return
    else:
        return


def bexp():
    global treeNum
    print('--' * treeNum, '逻辑表达式处理开始')
    treeNum += 2

    bterm()
    getnexttoken()
    if token == 'or':
        getnexttoken()
        bexp()
    elif token == 'then' or token == 'do':
        lasttoken()
        treeNum -= 2
        print('--' * treeNum, '逻辑表达式处理结束')
        return
    else:
        treeNum -= 2
        print('--' * treeNum, '逻辑表达式处理结束')
        return


def ifs():
    global treeNum
    print('--' * treeNum, 'if 处理开始')
    treeNum += 2

    getnexttoken()
    bexp()
    getnexttoken()
    if token != 'then':
        error('if 判断结束错误')
    getnexttoken()
    ST_SORT()
    if token == 'else':
        getnexttoken()
        ST_SORT()
        lasttoken()  # 回退一个
    else:
        lasttoken()

    treeNum -= 2
    print('--' * treeNum, 'if 处理结束')


def whiles():
    global treeNum
    print('--' * treeNum, 'while 处理开始')
    treeNum += 2

    # 处理
    getnexttoken()
    bexp()
    # lasttoken()
    getnexttoken()
    if token == 'do':
        getnexttoken()
        ST_SORT()
        lasttoken()
    else:
        error('while do > error')

    treeNum -= 2
    print('--' * treeNum, 'while 处理结束')


def fors():
    global treeNum
    print('--' * treeNum, 'for 处理开始')
    treeNum += 2

    getnexttoken()
    if not isIdentifider():
        error('for 标识符条件错误')
    getnexttoken()
    if token != ':=':
        error('for 起始条件错误')
    getnexttoken()
    aexp()
    if token == 'to':
        aexp()
    else:
        error('for to error')
    getnexttoken()
    aexp()
    if token == 'do':
        getnexttoken()
        ST_SORT()
    else:
        error('for do error')

    treeNum -= 2
    print('--' * treeNum, 'for 处理结束')


def repeat():
    global treeNum
    print('--' * treeNum, 'repeat 处理开始')
    treeNum += 2

    getnexttoken()
    ST_SORT()
    lasttoken()
    if token == 'until':
        getnexttoken()
        bexp()
    else:
        error('repeat')
    lasttoken()

    treeNum -= 2
    print('--' * treeNum, 'repeat 处理结束')


# 赋值处理
def assign():
    global treeNum
    print('--' * treeNum, '赋值处理开始')
    treeNum += 2

    obj = token
    getnexttoken()
    if token == ':=':
        getnexttoken()
        aexp()
    else:
        error('assign 赋值计算错误')

    treeNum -= 2
    print('--' * treeNum, '赋值处理结束')

    if token == ';' or token == 'until' or token == 'to' or token == 'do':
        return
    else:
        error('assign')


# 分类调用处理各个可执行语句
def ST_SORT():
    if isIdentifider():  # 为标识符  进入赋值或计算
        assign()
    elif token == 'if':
        ifs()
    elif token == 'while':
        whiles()
    elif token == 'for':
        fors()
        lasttoken()
    elif token == 'repeat':
        repeat()
    else:
        error("st-sort")
    getnexttoken()


# 错误处理
def error(reason):
    errorList.append([token, reason])


# 常量说明处理函数
def handle_const():
    global treeNum
    print('--' * treeNum, '常量说明处理开始')
    treeNum += 2

    while isIdentifider():
        name = token
        getnexttoken()
        if token == ':=':
            getnexttoken()
            if token.isdigit() or token.isalpha():
                changeSym(name, token, 'value')
            getnexttoken()
            if token == ';':
                getnexttoken()
                if not isIdentifider():
                    return
            else:
                error('常量声明错误')
        else:
            error('常量声明错误')
    error('常量声明错误')  # token 不标识符规范

    treeNum -= 2
    print('--' * treeNum, '常量说明处理结束')


# 变量说明处理函数
def handle_var():
    global treeNum
    print('--' * treeNum, '变量说明处理开始')
    treeNum += 2

    readyChange = []
    while isIdentifider():
        readyChange.append(token)
        getnexttoken()
        if token == ',':  # 仍有变量
            getnexttoken()  # 会再次进入while
        elif token == ':':  # 变量完毕
            getnexttoken()
            if token in wordCode[3:7]:  # 属于sample语言类型
                for rc in readyChange:  # 更新本行所有变量 类型
                    changeSym(rc, token, 'type')
                getnexttoken()
                if token == ';':  # 本行变量说明结束
                    # 处理readyChange
                    getnexttoken()
                    if token != 'begin':  # 本次变量说明是否结束
                        readyChange = []
                    else:
                        treeNum -= 2
                        print('--' * treeNum, '变量说明处理结束')

                        return
                else:
                    error('语句结束错误')
                    getnexttoken()
            else:
                error('变量类型错误')
        else:  # 非法中断结束
            error('变量声明错误')


# 语法分析总控程序
def parser():
    global token
    getnexttoken()
    while token != 'program':
        error('程序头部非法开头')
        getnexttoken()

    getnexttoken()
    if not isIdentifider():
        error("program后非程序名")

    getnexttoken()
    if token != ';':
        error("程序名后不是分号")

    getnexttoken()
    if token == 'const':
        getnexttoken()
        # 常量处理函数
        handle_const()
        getnexttoken()

    if token == 'var':
        getnexttoken()
        # 变量处理函数
        handle_var()

    while token != 'begin':
        error('可执行程序开始标识错误')
        getnexttoken()

    getnexttoken()
    while token != False and token != 'end' and (getnexttoken() != '.' and getnexttoken() != False):
        lasttoken()
        lasttoken()
        if getnexttoken() == False:
            error('程序结束错误')
        else:
            lasttoken()
            ST_SORT()


if __name__ == '__main__':
    parser()
    print()
    print("ERROR:")
    for error in errorList:
        print(error[0],' reason:',error[1])
