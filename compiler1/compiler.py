wordCode = ['', 'program', 'var', 'integer', 'bool', 'real', 'char', 'const', 'begin', 'if', 'then', 'else', 'while',
            'do', 'for', 'to', 'end', 'read', 'write', 'true', 'false', 'not', 'and', 'or', '+', '-', '*', '/', '<',
            '>', '<=', '>=', '==', '<>', 'id', '整常数', '实常数', '字符常数', '布尔常数', '=', ';', ',', '\'', '/*', '*/', ':', '(',
            ')', '.', ':=', 'repeat', 'until']
# 1-20 关键字  21-33 运算符  34 标识符  35-38 常数  39-49 界符 50-51 repeat util
tokenList = []
tokenList.append(["line", "word", "num"])
symList = []
symList.append(['name', 'token', 'type', 'value'])
errorList = []


def error(lineNumber, reason, s):  # 出错处理
    errorList.append([lineNumber, reason, s])


def isdelimeter(s):  # 是否在界符表中
    if s in wordCode[39:]:
        return True
    else:
        return False
    pass


def ins_token(lineNumber, s, num):  # 插入token表
    tokenList.append([lineNumber, s, num])


def ins_sym(name, token, type, value):  # 插入符号表
    # name token type value
    symList.append([name, token, type, value])


def isexist_sym(name):  # 是否在字符表中
    for sym in symList:
        if name in sym:
            return True
    return False


def hand_com():  # 注释处理
    pass


def iskeywords(s):  # 关键字判断
    if s in wordCode[1:21] or s in wordCode[50:]:
        return True
    return False


def recog_del():  # 界符判断
    pass


# 字母
def recog_id(lineNumber, line, x):  # 字母  标识符/关键字判断
    begin = x
    x += 1
    while line[x].isalpha() or line[x].isdigit() or line[x] == '_':
        x += 1
    s = line[begin:x]
    if iskeywords(s):  # 关键字
        ins_token(lineNumber, s, wordCode.index(s))
    else:  # 标识符
        if not isexist_sym(s):
            if s == 'True' or s == 'False':
                ins_sym(s, 38, wordCode[38], '')
            else:
                ins_sym(s, 34, wordCode[34], '')
        if s == 'True' or s == 'False':
            ins_token(lineNumber, s, 38)
        else:
            ins_token(lineNumber, s, 34)
    x -= 1
    return x


# 数字
def recog_dig(lineNumber, line, x):  # 数字判断
    begin = x
    x += 1
    if x < len(line):
        while line[x].isdigit():
            x += 1
        if line[x].isalpha() and line[x] not in wordCode:  # 数字+字母 错误
            while line[x].isalpha():
                x += 1
            s = line[begin:x]
            error(lineNumber, '非法命名', s)
            # errorList.append([lineNumber, s])
        elif line[x] == '.':  # 小数
            x += 1
            while line[x].isdigit():
                x += 1
            if line[x] == 'e':  # 12.e-5
                x += 1
                while line[x].isdigit():
                    x += 1
                if line[x] == '+' or line[x] == '-':
                    x += 1
                    while line[x].isdigit():
                        x += 1
                    if line[x] == '.':  # 12.3e3.5
                        x += 1
                        if line[x].isdigit():
                            while line[x].isdigit():
                                x += 1
                            s = line[begin:x]
                            if not isexist_sym(s):
                                ins_sym(s, 36, wordCode[36], s)
                            ins_token(lineNumber, s, 36)
                        else:  # 出错
                            s = line[begin:x]
                            error(lineNumber, '非法数字', s)
                            # errorList.append([lineNumber, s])
                    else:  # 12.3e-4
                        s = line[begin:x]
                        if not isexist_sym(s):
                            ins_sym(s, 36, wordCode[36], s)
                        ins_token(lineNumber, s, 36)
                elif line[x] == '.':  # 123.12e3.6
                    x += 1
                    while line[x].isdigit():
                        x += 1
                    s = line[begin:x]
                    if not isexist_sym(s):
                        ins_sym(s, 36, wordCode[36], s)
                    ins_token(lineNumber, s, 36)
                else:  # 12.3e or 12.3
                    s = line[begin:x]
                    if not isexist_sym(s):
                        ins_sym(s, 36, wordCode[36], s)
                    ins_token(lineNumber, s, 36)
            else:
                if line[x] == 'e':  # e
                    x += 1
                    while line[x].isdigit():
                        x += 1
                    if line[x] == '+' or line[x] == '-':
                        x += 1
                        while line[x].isdigit():
                            x += 1
                        if line[x] == '.':  # 12.3e3.5
                            x += 1
                            if line[x].isdigit():
                                while line[x].isdigit():
                                    x += 1
                                s = line[begin:x]
                                if not isexist_sym(s):
                                    ins_sym(s, 36, wordCode[36], s)
                                ins_token(lineNumber, s, 36)
                            else:  # 出错
                                s = line[begin:x]
                                error(lineNumber, '非法数字', s)
                                # errorList.append([lineNumber, s])
                        else:  # 12.3e-4
                            s = line[begin:x]
                            if not isexist_sym(s):
                                ins_sym(s, 36, wordCode[36], s)
                            ins_token(lineNumber, s, 36)
                    elif line[x] == '.':  # 123.12e3.6
                        x += 1
                        while line[x].isdigit():
                            x += 1
                        s = line[begin:x]
                        if not isexist_sym(s):
                            ins_sym(s, 36, wordCode[36], s)
                        ins_token(lineNumber, s, 36)
                    else:  # 12.3e or 12.3
                        s = line[begin:x]
                        if not isexist_sym(s):
                            ins_sym(s, 36, wordCode[36], s)
                        ins_token(lineNumber, s, 36)
                elif not line[x].isalpha():  # 正常结束
                    s = line[begin:x]
                    if not isexist_sym(s):
                        ins_sym(s, 36, wordCode[36], s)
                    ins_token(lineNumber, s, 36)
                else:  # .\e 后有其它值 错误
                    s = line[begin:x]
                    error(lineNumber, '非法数字', s)
                    # errorList.append([lineNumber, s])
        elif line[x] == 'e':  # 12e3
            x += 1
            if line[x].isdigit():
                while line[x].isdigit():
                    x += 1
                if line[x] == '+' or line[x] == '-' or line[x].isdigit():
                    x += 1
                    while line[x].isdigit():
                        x += 1
                    if line[x] == '.':  # 12e3.5
                        x += 1
                        if line[x].isdigit():
                            while line[x].isdigit():
                                x += 1
                            s = line[begin:x]
                            if not isexist_sym(s):
                                ins_sym(s, 36, wordCode[36], s)
                            ins_token(lineNumber, s, 36)
                        else:  # 出错
                            s = line[begin:x]
                            error(lineNumber, '非法数字', s)
                            # errorList.append([lineNumber, s])
                    else:  # 12e-4
                        s = line[begin:x]
                        if not isexist_sym(s):
                            ins_sym(s, 36, wordCode[36], s)
                        ins_token(lineNumber, s, 36)

                else:  # 12e or 12.3
                    s = line[begin:x]
                    if not isexist_sym(s):
                        ins_sym(s, 36, wordCode[36], s)
                    ins_token(lineNumber, s, 36)
            else:  # e 后有其它值 错误
                s = line[begin:x]
                error(lineNumber, '非法数字', s)
                # errorList.append([lineNumber, s])
        else:  # 整数
            s = line[begin:x]
            if not isexist_sym(s):
                ins_sym(s, 35, wordCode[35], s)
            ins_token(lineNumber, s, 35)
        # print('s:', s)
    return x


# 字符常数
def recog_str(lineNumber, line, x):
    """
    字符常数
    :param line:当前行内容
    :param x: 第x个字符
    :return:
    """
    x += 1
    begin = x
    while x < len(line) and line[x] != "'":
        x += 1
    s = line[begin:x]  # 不需要''
    if not isexist_sym(s):
        ins_sym(s, 37, wordCode[37], '')
    ins_token(lineNumber, s, 37)
    return x


def token(lines):
    lineNumber = 0
    for line in lines:
        x = 0
        while x < len(line):
            # print(line[x])
            if line[x] == ' ':  # 空格
                x += 1
                while line[x] == ' ':
                    x += 1
                x -= 1
            elif line[x].isdigit():  # 数字
                if not line[x - 1].isalpha():
                    x = recog_dig(lineNumber, line, x) - 1
            elif line[x] == "'":  # 字符常数
                x = recog_str(lineNumber, line, x)
            elif line[x].isalpha():  # 字母
                x = recog_id(lineNumber, line, x)
            else:
                if isdelimeter(line[x:x + 2]):  # :=
                    ins_token(lineNumber, line[x:x + 2], wordCode.index(line[x:x + 2]))
                    x += 1
                elif line[x] in wordCode[21:34]:
                    ins_token(lineNumber, line[x], wordCode.index(line[x]))  # 符号
                elif isdelimeter(line[x]):
                    ins_token(lineNumber, line[x], wordCode.index(line[x]))
            x += 1
        lineNumber += 1


def outputToken():
    print('TOKENLIST:')
    f = open('../compiler1/TOKEN.txt', 'w+')
    for t in tokenList:
        print("%-10s%-15s%s" % (t[0], t[1], t[2]))
        f.write("%-10s%-15s%s\n" % (t[0], t[1], t[2]))
    print()
    f.close()


def outputSym():
    print('SYMLIST:')
    f = open('../compiler1/SYM.txt', 'w+')
    for t in symList:
        print("%-15s%-10s%-20s%s" % (t[0], t[1], t[2], t[3]))
        f.write("%-15s%-10s%-20s%s\n" % (t[0], t[1], t[2], t[3]))
    print()
    f.close()


def outputError():
    print('ERRORLIST:')
    f = open('../compiler1/ERROR.txt', 'w+')
    f.write("ERRORLIST:\n")
    for t in errorList:
        print("%s:\t%s:  %s" % (t[0], t[1], t[2]))
        f.write("%s:\t%s:  %s\n" % (t[0], t[1], t[2]))
    print()
    f.close()


def removeComments(fileName):  # 去除注释
    resultPath = "../compiler1/RESULT.txt"
    with open(fileName, 'r') as f:
        content = f.read()
        print(content)
    print('*******************')
    result = ''
    x = 0
    while x < len(content):  # 去除/**/注释
        if content[x:x + 2] == '/*':
            x += 2
            while content[x:x + 2] != '*/':
                x += 1
            x += 2  # 后移两位 到*/后面
        result += content[x]
        x += 1
    with open(resultPath, 'w+') as f:
        f.write(result)
    # print("r1:\n", result)
    with open(resultPath, 'r') as f:
        content = f.readlines()
        # print(content)
    result = []
    for line in content:  # 去除//注释
        for x in range(len(line)):
            if line[x:x + 2] == '//':
                line = line[:x] + '\n'
        result.append(line)
    with open(resultPath, 'w+') as f:
        for r in result:
            f.write(r)
    f.close()
    return result


if __name__ == '__main__':
    # fileName = 'E:\CQUT\编译原理\编译原理教学辅助系统\TestFile\sample.txt'
    # fileName = 'sample.txt'
    fileName = input("sample文件地址：")  # sample.txt
    lines = removeComments(fileName)
    # print(lines)
    token(lines)

    outputToken()
    outputSym()
    outputError()
