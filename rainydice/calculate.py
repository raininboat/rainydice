# -*- coding: utf-8 -*-
'''
   ___  ___   _____  ____  __
  / _ \/ _ | /  _/ |/ /\ \/ /
 / , _/ __ |_/ //    /  \  / 
/_/|_/_/ |_/___/_/|_/   /_/  
                             
    四则运算实现(含d运算)
'''
import random
class RPN(object):
    def RPNchange(self,Input):
        # 符号优先级
        calsign = {
            '$' : 0 , '(' : 0,
            '+' : 1 , '-' : 1,
            '*' : 2 , '/' : 2,
            'd' : 3 , 'D' : 3
        }
        # 数字
        calnum = {
            '1' : 1 , '2' : 2,
            '3' : 3 , '4' : 4,
            '5' : 5 , '6' : 6,
            '7' : 7 , '8' : 8,
            '9' : 9 , '0' : 0
        }
        calculate = []
        sign = []
        sign.append('$')
        number = None
        tmp = ''
        strlen = len(Input)
        for i in range(strlen):
            tmp = Input[i]
            if tmp in calnum:
                if not number:
                    number = 0
                number = number * 10 + calnum[tmp]
            elif tmp == '(':
                if type(number) == int:
                    calculate.append(number)
                    number = None
                sign.append('(')
            elif tmp == ' ':
                pass
            elif tmp in calsign:
                if type(number) == int:
                    calculate.append(number)
                    number = None
                lastSign = sign[len(sign)-1]
                if lastSign != '(':
                    # 当前运算符和栈顶运算符比较优先级
                    while calsign[tmp] <= calsign[lastSign]:
                        calculate.append(sign.pop())
                        lastSign = sign[len(sign)-1]
                        if lastSign == '$':
                            break
                sign.append(tmp)
            elif tmp == ')':
                if type(number) == int:
                    calculate.append(number)
                    number = None
                lastSign = sign[len(sign)-1]
                while lastSign != '(':
                    if lastSign =='$':
                        raise(Exception,'符号不匹配！')
                    calculate.append(sign.pop())
                    lastSign = sign[len(sign)-1]
                sign.pop()
            else:
                if type(number) == int:
                    calculate.append(number)
                    number = None
                while sign[len(sign)-1] != '$':
                    if sign[len(sign)-1] == '(':
                        raise(Exception,'四则运算表达式错误!')
                    calculate.append(sign.pop())
                break
        if type(number) == int :
            calculate.append(number)
            number = None
        while sign[len(sign)-1] != '$':
            if sign[len(sign)-1] == '(':
                raise(Exception,'四则运算表达式错误！')
            calculate.append(sign.pop())
        return calculate

    def RPNcal(self,cal):
        
        def rand(x=1,y=1):
            result = 0
            for i in range(x):
                result = result + random.randint(1,y)
            return result
        a = []
        x = 0
        y = 0
        tmp = None
        calsign = {
            '+' : 1 , '-' : 1,
            '*' : 2 , '/' : 2,
            'd' : 3 , 'D' : 3
        }
        for i in range(len(cal)):
            tmp = cal[i]
            if type(tmp) == int:
                a.append(tmp)
                tmp = None
            elif calsign[tmp]:
                y = a.pop()
                x = a.pop()
                if x == None:
                    raise(Exception,'后缀表达式错误！')
                if tmp == '+':
                    res = x + y
                    a.append(res)
                elif tmp == '-':
                    res = x-y
                    a.append(res)
                elif tmp == '*':
                    res = x*y
                    a.append(res)
                elif tmp == '/':
                    res = x//y
                    a.append(res)
                elif tmp == 'D' or tmp =='d':
                    res = rand(x,y)
                    a.append(res)
                tmp = None
            else:
                break
        return a.pop()
    def calculate(self,string):
        temp = string[0]
        if temp == '+' or temp == '-':
            string = '0'+string
        elif temp == '*' or temp == '/' or temp == 'D' or temp == 'd':
            string='1'+string
        temp = string[-1]
        if temp == 'D' or temp =='d':
            string = string + '100'
        while temp == '(' or temp == '（':
            string = string[:-1]
            temp = string[-1]
        # print(string)
        cal = self.RPNchange(string)
        # print(cal)
        result = self.RPNcal(cal)
        return result
#a = RPN()
#cal = '3*5d6+2'
#print(a.calculate(cal))