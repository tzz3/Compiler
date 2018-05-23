wordCode = ['', 'program', 'var', 'integer', 'bool', 'real', 'char', 'const', 'begin', 'if', 'then', 'else', 'while',
            'do', 'for', 'to', 'end', 'read', 'write', 'true', 'false', 'not', 'and', 'or', '+', '-', '*', '/', '<',
            '>', '<=', '>=', '==', '<>', 'id', '整常数', '实常数', '字符常数', '布尔常数', '=', ';', ',', '\'', '/*', '*/', ':', '(',
            ')', '.', ':=', 'repeat', 'until']
# 1-20 关键字  21-33 运算符  34 标识符  35-38 常数  39-49 界符 50-51 repeat util

tokenList = []
symList = []

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


def semanticCheck():
    pass


def dispose():
    pass


if __name__ == '__main__':
    # 静态语义检查
    # 语义处理
    pass
