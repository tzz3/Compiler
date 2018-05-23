import compiler3.compiler3

wordCode = ['', 'program', 'var', 'integer', 'bool', 'real', 'char', 'const', 'begin', 'if', 'then', 'else', 'while',
            'do', 'for', 'to', 'end', 'read', 'write', 'true', 'false', 'not', 'and', 'or', '+', '-', '*', '/', '<',
            '>', '<=', '>=', '==', '<>', 'id', '整常数', '实常数', '字符常数', '布尔常数', '=', ';', ',', '\'', '/*', '*/', ':', '(',
            ')', '.', ':=', 'repeat', 'until']
# 1-20 关键字  21-33 运算符  34 标识符  35-38 常数  39-49 界符 50-51 repeat util
rop = ['>', '<', '>=', '<=', '<>', '==']
aop = ['+', '-', '*', '/']
bop = ['not', 'and', 'or']
tokenList = []
symList = []
errorList = []
t = -1
token = ''
treeNum = 2

intermediate = {}
K = 0  # 四元式序号
n = 1  # Tn

tokenPath = "../compiler1/TOKEN.txt"
with open(tokenPath, 'r') as f:
    tk = f.readlines()
    for k in tk:
        split = k.split()
        if len(split) == 3:
            tokenList.append(split[1])
    tokenList = tokenList[1:]

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
                if len(sym) == 3:
                    sym.append(value)
                else:
                    sym[3] = value
            if type == 'type':  # 修改类型
                sym[2] = value


"""算术表达式"""


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


"""逻辑表达式"""


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


"""控制语句"""


def ifs():
    global treeNum
    global t
    global n
    global K
    print('--' * treeNum, 'if 处理开始')
    treeNum += 2

    begin = t
    getnexttoken()
    bexp()
    end = t
    s = tokenList[begin + 1:end + 1]
    # print(s)
    rpn = toRPN(s)
    # print(rpn)

    tc, fc = rpntoimd(rpn)  # 需要回填列表
    # print(tc, fc)
    backfill(tc)

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

    backfill(fc)  # if 处理完毕错误跳转回传

    treeNum -= 2
    print('--' * treeNum, 'if 处理结束')


def whiles():
    global treeNum
    global t
    global n
    global K
    print('--' * treeNum, 'while 处理开始')
    treeNum += 2

    # 处理
    getnexttoken()
    begin = t
    bexp()
    end = t

    s = tokenList[begin:end + 1]
    rpn = toRPN(s)

    tc, fc = rpntoimd(rpn)

    getnexttoken()
    if token == 'do':
        getnexttoken()
        ST_SORT()
        lasttoken()
    else:
        error('while do > error')

    backfill(fc)  # while 错误跳转回填

    treeNum -= 2
    print('--' * treeNum, 'while 处理结束')


def fors():
    global treeNum
    global t
    global n
    global K
    print('--' * treeNum, 'for 处理开始')
    treeNum += 2

    getnexttoken()
    begin = t
    i = token
    kf = K
    if not isIdentifider():
        error('for 标识符条件错误')
    getnexttoken()
    if token != ':=':
        error('for 起始条件错误')
    getnexttoken()
    aexp()
    end = t
    s = tokenList[begin:end]
    # print(s)
    rpn = toRPN(s)
    # print(rpn)
    rpntoimd(rpn)
    kf = K

    bf = []
    if token == 'to':
        begin = t
        aexp()
        end = t
        s = tokenList[begin + 1:end + 2]
        arg1 = intermediate[K - 1][3]
        if len(s) > 1:
            rpn = toRPN(s)
            rpntoimd(rpn)
            arg2 = intermediate[K - 1][3]
        else:
            arg2 = s[0]
        itd = ['j>', arg1, arg2, -1]
        bf.append(K)
        intermediate[K] = itd
        K += 1
    else:
        error('for to error')

    getnexttoken()
    getnexttoken()

    if token == 'do':
        getnexttoken()
        ST_SORT()

    else:
        error('for do error')

    # for 回跳
    itd = ['+', i, 1, 'T' + str(n)]
    n += 1
    intermediate[K] = itd
    K += 1
    itd = [':=', 'T' + str(n - 1), '_', i]  # i+=1
    intermediate[K] = itd
    K += 1
    itd = ['j', '_', '_', str(kf)]  # i+=1  返回for起点
    n += 1
    intermediate[K] = itd
    K += 1

    # backfill
    backfill(bf)

    treeNum -= 2
    print('--' * treeNum, 'for 处理结束')


def repeat():
    global treeNum
    global t
    global n
    global K
    print('--' * treeNum, 'repeat 处理开始')
    treeNum += 2

    getnexttoken()
    # a
    TC = K
    ST_SORT()
    lasttoken()

    bf = []
    if token == 'until':
        getnexttoken()
        begin = t
        bexp()
        end = t - 1
        # print(token)
        # print(begin, end)
        if end - begin <= 3:
            s = tokenList[begin:end]
        else:
            s = tokenList[begin:end - 1]
        # print(s)
        rpn = toRPN(s)
        # print(rpn)

        stack = []
        for r in rpn:
            if not isSymbol(r):
                stack.append(r)
            else:
                arg2 = stack.pop()
                arg1 = stack.pop()
                if r in rop:
                    itd = ['j' + r, arg1, arg2, TC]
                else:
                    if r == ':=':
                        itd = [r, arg2, '_', arg1]
                    else:
                        itd = [r, arg1, arg2, 'T' + str(n)]
                        stack.append('T' + str(n))
                        n += 1
                intermediate[K] = itd
                K += 1
    else:
        error('repeat')
    lasttoken()

    treeNum -= 2
    print('--' * treeNum, 'repeat 处理结束')


# 类型检查
def typecheck(name, type):
    for s in symList:
        if name in s:
            if s[2] != type:
                return False
            else:
                return True
    return False


# 操作数
def isConvert(e):
    if e.isdigit():
        return True
    elif e.isalpha() and e not in bop:
        return True
    else:
        return False


# 运算符
def isSymbol(e):
    if e in [':=', '+', '-', '*', '/', '>', '<', '>=', '<=', '<>', '==', 'not', 'and', 'or']:
        return True
    else:
        return False


# 优先级比较
def priority(a, b):  # b优先级高 return true
    p = ['(', ')', '*', '/', '-', '+', ':=', '>', '<', '>=', '<=', '<>', '==', 'not', 'and', 'or']
    if p.index(a) >= p.index(b):
        return True
    else:
        return False


# 逆波兰式转换
def toRPN(sentence):  # reverse polish notation 逆波兰式
    RPN = []
    stack = []
    top = 0
    for ch in sentence:
        if isConvert(ch):
            RPN.append(ch)
        elif isSymbol(ch) or ch == "(":
            # 先出栈
            if top > 0 and priority(ch, stack[top - 1]) and stack[top - 1] != '(':  # ch优先级低
                while top > 0 and priority(ch, stack[top - 1]) and stack[top - 1] != '(':
                    RPN.append(stack[top - 1])
                    top -= 1

            # 进栈
            if top == len(stack):
                top += 1
                stack.append(ch)
            elif top < len(stack):
                top += 1
                stack[top - 1] = ch
        elif ch == ')':
            # 弹出
            while top >= 0:
                if stack[top - 1] == '(':
                    top -= 1
                    break

                if stack[top - 1] != '(':
                    RPN.append(stack[top - 1])
                top -= 1
    if top > 0:  # 循环完毕 将栈内元素输出
        while top > 0:
            if stack[top - 1] != '(':
                RPN.append(stack[top - 1])
            top -= 1
    return RPN


"""intermediate"""


# 波兰式转换为四元式
def rpntoimd(rpn):
    global intermediate
    global n
    global K

    stack = []
    tc = []  # 逻辑正确
    fc = []  # 错误

    if len(rpn) == 1:
        itd = ['jnz', rpn[0], '_', -1]
        tc.append(K)
        intermediate[K] = itd
        K += 1
        itd = ['j', '_', '_', -1]
        fc.append(K)
        intermediate[K] = itd
        K += 1
        return tc, fc

    iK = -1
    for r in rpn:
        if not isSymbol(r):
            stack.append(r)
        else:
            if r in rop:
                arg2 = stack.pop()
                arg1 = stack.pop()
                itd = ['j' + r, arg1, arg2, K + 2]
                intermediate[K] = itd
                K += 1
                itd = ['j', '_', '_', iK]
                fc.append(K)
                intermediate[K] = itd
                K += 1
            elif r in bop:  # not or and
                if r == 'or':
                    tc.append(K - 2)  # 跳转到content
                    fc.append(K - 2)  # 跳转到当前运行完成
                elif r == 'not':
                    arg = stack.pop()
                    itd = ['jnz', 'not ' + arg, '_', -1]
                    fc.append(K)
                    intermediate[K] = itd
                    K += 1
                else:  # and
                    stack = []
                pass
            else:
                arg2 = stack.pop()
                arg1 = stack.pop()
                if r == ':=':
                    itd = [r, arg2, '_', arg1]
                else:
                    itd = [r, arg1, arg2, 'T' + str(n)]
                    stack.append('T' + str(n))
                    n += 1
                intermediate[K] = itd
                K += 1
    return tc, fc


# 跳转回填
def backfill(bf):
    for b in bf:  # 处理完毕错误跳转回传
        intermediate[b][3] = K


# 赋值处理 算术表达式
def assign():
    global treeNum
    global t
    global intermediate
    global n
    global K
    print('--' * treeNum, '赋值处理开始')
    treeNum += 2
    begin = t
    obj = token
    getnexttoken()
    if token == ':=':
        getnexttoken()

        if token.isdigit():
            if typecheck(obj, 'integer'):
                changeSym(obj, token, 'value')
                pass
            else:
                error(obj + ' type error')
        elif token.isalpha():
            if typecheck(obj, 'char'):
                changeSym(obj, token, 'value')
            else:
                error(obj + 'type error')
        aexp()
    else:
        error('assign 赋值计算错误')
    end = t
    s = tokenList[begin:end]
    # print(s)
    s1 = s[:s.index(':=') + 1]
    s2 = s[s.index(':=') + 1:]

    rpn = toRPN(s2)
    # print(rpn)
    stack = []
    for r in rpn:
        if not isSymbol(r):
            stack.append(r)
        else:
            arg2 = stack.pop()
            arg1 = stack.pop()
            itd = [r, arg1, arg2, 'T' + str(n)]
            stack.append('T' + str(n))
            n += 1
            intermediate[K] = itd
            K += 1

    if len(rpn) == 1:
        itd = [s1[1], s2[0], '_', s1[0]]
    else:
        itd = [s1[1], 'T' + str(n - 1), '_', s1[0]]
    intermediate[K] = itd
    K += 1

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
    global token
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
                    treeNum -= 2
                    print('--' * treeNum, '常量说明处理结束')
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
        # getnexttoken()

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


# 输出符号表
def outputSym():
    global symList
    print('SYMLIST:')
    print("%-15s%-10s%-20s%s" % ('name', 'token', 'type', 'value'))
    for t in symList:
        if len(t) == 3:
            print("%-15s%-10s%-20s%s" % (t[0], t[1], t[2], ''))  # , t[3]
        else:
            print("%-15s%-10s%-20s%s" % (t[0], t[1], t[2], t[3]))
    print()


if __name__ == '__main__':
    parser()
    print("\nERROR:")
    for error in errorList:
        print(error[0], ' reason:', error[1])
    print()
    # print(symList)

    outputSym()

    print("生成四元式：")
    for i in intermediate:
        value = intermediate[i]
        # print(i, intermediate[i])
        print('(%-2s)  (%-2s, %-2s, %-2s, %-2s)' % (i, value[0], value[1], value[2], value[3]))
