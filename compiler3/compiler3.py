class NFA:
    def __init__(self, start, ch, end):
        self.start = start
        self.ch = ch
        self.end = end

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getCh(self):
        return self.ch

    def getAll(self):
        return self.start, self.ch, self.end


expression = "(a*|b)*b"  # *b|(c|d)*


def inputExpression():
    global expression
    expression = input("expression:")


result = False


def verify():  # 正规式验证
    flag = 0
    index = 1
    global result
    if expression[0] == "(" or expression[0].isdigit() or expression[0].isalpha():
        if expression[0] == '(':
            flag += 1
    else:
        return False
    while index < len(expression) - 1:
        current = expression[index]
        last = expression[index - 1]
        if index + 1 < len(expression):
            after = expression[index + 1]
        else:
            after = False
        if current == "(":
            flag += 1
        elif current == ')':
            flag -= 1

        elif current == "|":
            if last == '*' or last == ')' or last.isdigit() or last.isalpha():
                if after == '*' or after == '(' or after.isdigit() or after.isalpha() or after == False:
                    result = True
                else:
                    return False
            else:
                return False
        elif current == "*":
            if last == ')' or last.isdigit() or last.isalpha():
                if after == '*' or after == '(' or after == ')' or after.isdigit() or after.isalpha() or after == '|' or after == False:
                    result = True
                else:
                    return False
            else:
                return False
        if flag < 0:
            return False
        index += 1

    current = expression[index]
    if current == ')' or current.isdigit() or current.isalpha() or current == '*':
        if current == ')':
            flag -= 1
            if flag == 0:
                result = True
                return result
            else:
                return False
        else:
            if flag == 0:
                result = True
                return result
            else:
                return False
    else:
        return False


def toInfix():  # 转为中缀表达式
    global expression
    index = 1
    while index < len(expression):
        a = expression[index - 1]
        b = expression[index]
        if isConvert(a) and b == '(':
            expression = expression[:index] + '.' + expression[index:]
        if (a == '*' and isConvert(b)) or (b == '*' and isConvert(a)):
            expression = expression[:index] + '.' + expression[index:]
        if (a == '*' and b == '(') or (a == ')' and b == '('):
            expression = expression[:index] + '.' + expression[index:]
        if isConvert(a) and isConvert(b):
            expression = expression[:index] + '.' + expression[index:]
        index += 1


def toRPN():  # reverse polish notation 逆波兰式
    global expression
    RPN = ''
    stack = []
    top = 0
    for ch in expression:
        if isConvert(ch):
            RPN += ch
        elif isOperate(ch) or ch == "(":
            # 先出栈
            if top > 0 and priority(ch, stack[top - 1]) and stack[top - 1] != '(':  # ch优先级低
                while top > 0 and priority(ch, stack[top - 1]) and stack[top - 1] != '(':
                    RPN += stack[top - 1]
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
                    RPN += stack[top - 1]
                top -= 1
    if top > 0:  # 循环完毕 将栈内元素输出
        while top > 0:
            if stack[top - 1] != '(':
                RPN += stack[top - 1]
            top -= 1
    return RPN


def priority(a, b):  # b优先级高 return true
    p = ['(', '*', '.', '|']
    if p.index(a) > p.index(b):
        return True
    else:
        return False


def isConvert(e):
    if e.isdigit():
        return True
    elif e.isalpha():
        return True
    else:
        return False


def isOperate(e):
    if e == '*' or e == '|' or e == '.':
        return True
    else:
        return False


type = -1
nfa = []
part = []
index = 0


def toNFA(rpn):  # nfa
    global type
    global index
    while index < len(rpn):
        r = rpn[index]
        # print(r)
        if isConvert(r):
            handle(r)
        elif r == '*':
            handle1()
        elif r == '.':
            pass
        elif r == '|':
            handle2()
        index += 1


def big(nfa):
    startBig = nfa[0].getStart()
    endBig = nfa[0].getEnd()
    for n in nfa:
        if startBig < n.getStart():
            startBig = n.getStart()
        if endBig < n.getEnd():
            endBig = n.getEnd()
    return startBig, endBig


def handle(ch):  #
    global type
    global index
    t = type
    type += 1
    begin = type
    type += 1
    if t > 1 and rpn[index + 1] == '.':
        nfa.append(NFA(t, '#', begin))
        if len(part) >= 1:
            begin = part[-1][0]
            part.remove(part[-1])

    nfa.append(NFA(begin, ch, type))
    part.append([begin, type])


def handle1():  # *
    global type
    startBig, endBig = big(nfa)
    # print(type)
    type += 1
    begin = type
    type += 1
    end = type

    nfa.append(NFA(endBig, '#', startBig))
    nfa.append(NFA(begin, '#', startBig))
    nfa.append(NFA(endBig, '#', end))
    nfa.append(NFA(begin, '#', end))

    part.remove([startBig, endBig])
    part.append([begin, end])


def handle2():  # |
    global type
    a = part[-1]
    b = part[-2]
    type += 1
    begin = type
    type += 1
    end = type

    nfa.append(NFA(begin, '#', a[0]))
    nfa.append(NFA(begin, '#', b[0]))
    nfa.append(NFA(a[1], '#', end))
    nfa.append(NFA(b[1], '#', end))

    part.remove(a)
    part.remove(b)
    part.append([begin, end])


def handle3():  # .
    pass


dfa = []
I = []
top = 0


def toDFA():
    global top

    word = getWord()  # 获取所有输入字符 a,b
    i = Closure(['X'])
    I.append(i)
    # top += 1
    while top < len(I):
        line = []
        i = I[top]  # 获取第一列中为计算的值
        top += 1
        line.append(i)
        flag = len(word)
        for w in word:
            J = JClosure(i, w)  # 计算J
            f = Closure(J)  # 计算Closure

            line.append(f)

            if f not in I:
                if len(f) != 0:
                    I.append(f)  # 添加到第一列
            else:
                flag -= 1

        m = 1
        while m < len(line):  # 去除空行
            if len(line[m]) != 0:
                dfa.append(line)
                break
            m += 1


def find(start, key):
    closure = []
    flag = 0
    while flag == 0:
        flag = 1
        for n in nfa:
            ch = n.getCh()
            s = n.getStart()
            e = n.getEnd()
            if (s in start or s in closure) and ch == '#' and e not in closure and e != 'X':
                flag = 0
                closure.append(e)
            # if (s in start) and (ch == '#' or ch == key) and e not in closure and e != 'X':
            #     flag = 0
            #     closure.append(e)
            if (s in start) and ch == key and e not in closure and e != 'X':
                flag = 0
                closure.append(e)
    return closure


def Closure(X):
    closure = []
    for x in X:
        closure.append(x)
    flag = 0
    while flag == 0:
        flag = 1
        for n in nfa:
            ch = n.getCh()
            s = n.getStart()
            e = n.getEnd()
            if (s in X or s in closure) and ch == '#' and e not in closure:
                flag = 0
                closure.append(e)
    return closure


def JClosure(J, word):
    jclosure = []
    for n in nfa:
        ch = n.getCh()
        s = n.getStart()
        e = n.getEnd()
        if s in J and ch == word and e not in jclosure:
            jclosure.append(e)
    return jclosure


def getWord():
    word = []
    for n in nfa:
        if n.getCh() != '#' and (n.getCh() not in word):
            word.append(n.getCh())
    return word


def toMFA():
    pass


if __name__ == '__main__':
    inputExpression()

    result = verify()
    print("正规式验证", expression, ":", result)
    toInfix()
    print("中缀表达式:", expression)
    rpn = toRPN()
    print("逆波兰式:", rpn)

    toNFA(rpn)
    begin = part[0][0]
    end = part[0][1]
    nfa.append(NFA('X', '#', begin))
    nfa.append(NFA(end, '#', 'Y'))
    for n in nfa:
        print(n.getAll())
    print("\n开始状态集：", part[0][0])
    print("结束状态集：", part[0][1])

    print("符号：", getWord())
    toDFA()
    print()
    for d in dfa:
        print(d)
    # print(Closure(['X']))
