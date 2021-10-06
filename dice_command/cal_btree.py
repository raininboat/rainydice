# -*- coding: utf-8 -*-
'''
   ___  ___   _____  ____  __
  / _ \/ _ | /  _/ |/ /\ \/ /
 / , _/ __ |_/ //    /  \  / 
/_/|_/_/ |_/___/_/|_/   /_/  
                             
    四则运算实现(含d运算)

    Copyright (C) 2021  RainyZhou  
                        Email: thunderain_zhou@163.com

    This file is part of RainyDice.

    RainyDice is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    RainyDice is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with RainyDice.  If not, see <https://www.gnu.org/licenses/>

'''
from random import randint as __randint
class __BTree(object):
    def __init__(self,data = None):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None
    def insert_left(self,left):
        self.left = left
        self.left.parent = self
    def insert_right(self,right):
        self.right = right
        self.right.parent = self
    def set_data(self,data):
        self.data = data
    def get_data(self):
        return self.data
    def get_parent_data(self):
        if self.parent == None:
            return None
        return self.parent.data
    def goto_parent(self,node):
        if node.parent != None:
            return node.parent,True
        else:
            return node,False
    def goto_left(self):
        if self.left != None:
            return self.left , True
        else:
            return self,False
    def goto_right(self):
        if self.right != None:
            return self.right , True
        else:
            return self , False
    def get_parent(self):
        if self.parent != None:
            return self.parent.data
        else:
            return None
    def get_left(self):
        if self.left != None:
            return self.left.data
        else:
            return None
    def get_right(self):
        if self.right != None:
            return self.right.data
        else:
            return None
    def goto_root(self):
        tmp,status = self.goto_parent(self)
        while status != False:
            tmp , status = self.goto_parent(tmp)
        return tmp
    def inorder(self,node):
        #tmp = self.goto_root()
        if node == None:
            return []
        result = [self]
        left_item = self.inorder(node.left)
        right_item = self.inorder(node.right)
        return left_item + result + right_item
    def postorder(self,node):  # 后序遍历
        if node is None:
            return []
        result = [node]
        left_item = self.postorder(node.left)
        right_item = self.postorder(node.right)
        return left_item + right_item + result
    def preorder(self,node):  # 先序遍历
        if node is None:
            return []
        result = [node]
        left_item = self.preorder(node.left)
        right_item = self.preorder(node.right)
        return result + left_item + right_item



def __split(string:str):
    splitData = []
    sign = (
        '+','-','*','/','(',')',
        'd','q','p','b','k',
        'a','m'
    )
    num = ('1','2','3','4','5','6','7','8','9','0')
    defaultDiceRollSide = '100'   # 默认骰(D)
    defaultDicePoolAdd = '10'
    # defaultDicePoolSuccess = 8
    # defaultDicePoolSide = 10
    # MaxDice = 9999      # 设置的最大投掷数量结果
    MaxSplit = 999      # 最大切片数（即表达式运算长度限制）
    pointer = 0         # 表达式扫描部分的指针    
    for i in range(len(string)):
        if string[i] in sign:
            if pointer < i:
                splitData.append(string[pointer:i])
            elif pointer == i:      # 连续两个符号（判断是否需要添加默认值）
                if string[i] == '(':      # 当前为'('无需改变
                    pass
                elif string[i] in ('+','-','*','/',')','d','q','p','b','k','a','m'):
                    if i == 0:
                        if string[i] in ('-','+','*','/'):      # 加减乘除这类前面添加 0
                            splitData.append('0')
                        elif string[i] in ('d','p','b','a'):    # 投掷表达式前面添加 1 (默认至少骰1个骰子)
                            splitData.append('1')
                        elif string[i] in ('k','q','m'):        # 不能直接是 k，q，m 这类投掷表达式的装饰器
                            raise UserWarning('Input_Raw_Invalid','输入内容错误:含有不完整的投掷表达式')
                    else:
                        if splitData[-1] ==')':                   # 如果前一位是')'，则无需进行默认值添加
                            pass
                        elif splitData[-1] == 'd':                # ---d100
                            splitData.append(defaultDiceRollSide)       # d后面添加默认面数
                        elif splitData[-1] == 'a':                # ---a10
                            splitData.append(defaultDicePoolAdd)       # a后面添加默认加骰线
                        elif splitData[-1] in ('p','b'):
                            splitData.append("1")                   # xxxp1 xxxb1
                        elif string[i] in ('a','d','b','p'):
                            splitData.append('1')                   # 1dxxx 1axxx 1pxxx 1bxxx
            splitData.append(string[i])
            pointer = i+1
        else:
            if string[i] not in num:
                raise UserWarning('Input_Unknown_Sign','含有未知符号:'+string[i])
    if pointer < len(string):
        splitData.append(string[pointer:])      # 最后一个数字写入
    elif pointer == len(string):                # 表达式最后一位是符号
        if splitData[-1] ==')':                   # 如果前一位是')'，则无需进行默认值添加
            pass
        elif splitData[-1] == 'd':                # ---d100
            splitData.append(defaultDiceRollSide)       # d后面添加默认面数
        elif splitData[-1] == 'a':                # ---a10
            splitData.append(defaultDicePoolAdd)       # a后面添加默认加骰线
        elif splitData[-1] in ('p','b'):
            splitData.append('1')  
    if len(splitData) > MaxSplit:
        raise UserWarning('Split_Too_Much','表达式过长或过复杂:当前分片数量['+str(len(splitData))+']')
    return splitData
def __RPNchange(Input):
    # 符号优先级
    calsign = {
        '$' : 0 , '(' : 0,
        '+' : 1 , '-' : 1,
        '*' : 2 , '/' : 2,
        'd' : 3 , 'k':3, 'q':3,'p':3,'a':3,'m':3,'b':3  
    }
    
    calculate = []
    sign = []
    sign.append('$')
    tmp = ''
    for tmp in Input:
        if str.isdecimal(tmp):
            tmp_tree = __BTree(int(tmp))
            calculate.append(tmp_tree)
        elif tmp == '(':
            sign.append('(')
        elif tmp == ' ':
            pass
        elif tmp in calsign:
            lastSign = sign[-1]
            if lastSign != '(':
                # 当前运算符和栈顶运算符比较优先级
                while calsign[tmp] <= calsign[lastSign]:
                    #calculate.append(sign.pop())
                    tmp_sign = sign.pop()
                    tmp_tree = __BTree(tmp_sign)
                    tmp_tree.insert_right(calculate.pop())
                    tmp_tree.insert_left(calculate.pop())
                    calculate.append(tmp_tree)
                    lastSign = sign[len(sign)-1]
                    if lastSign == '$':
                        break
            sign.append(tmp)
        elif tmp == ')':
            lastSign = sign[-1]
            while lastSign != '(':
                if lastSign =='$':
                    raise(Exception,'符号不匹配！')
                # calculate.append(sign.pop())
                tmp_sign = sign.pop()
                tmp_tree = __BTree(tmp_sign)
                tmp_tree.insert_right(calculate.pop())
                tmp_tree.insert_left(calculate.pop())
                calculate.append(tmp_tree)
                lastSign = sign[len(sign)-1]
            sign.pop()
        else:
            while sign[len(sign)-1] != '$':
                if sign[len(sign)-1] == '(':
                    raise(Exception,'四则运算表达式错误!')
                # calculate.append(sign.pop())
                tmp_sign = sign.pop()
                tmp_tree = __BTree(tmp_sign)
                tmp_tree.insert_right(calculate.pop())
                tmp_tree.insert_left(calculate.pop())
                calculate.append(tmp_tree)
            break
    while sign[len(sign)-1] != '$':
        if sign[len(sign)-1] == '(':
            raise(Exception,'四则运算表达式错误！')
        # calculate.append(sign.pop())
        tmp_sign = sign.pop()
        tmp_tree = __BTree(tmp_sign)
        tmp_tree.insert_right(calculate.pop())
        tmp_tree.insert_left(calculate.pop())
        calculate.append(tmp_tree)
    tree = calculate.pop()
    return tree.postorder(tree)

# diceCount 投掷个数
# diceSide 投掷面数
# diceMax 取最大的数量(k)
# diceMin 取最小的数量(q)
def __diceRoll(diceCount,diceSides,diceMax=None,diceMin=None):
    # print(diceCount,diceSides,diceMax,diceMin)
    MaxDice = 9999      # 最多面数、最多投掷个数

    if diceCount > MaxDice or diceSides > MaxDice :
        raise(UserWarning('Roll_Too_Big','投掷次数或单个面数过大'))
    elif diceCount == 0 or diceSides == 0:
        raise (UserWarning('Zero_Dice_Error','投掷个数不能为0'))
    if diceMax != None:
        step = '{'
        rollStep = []
        rolltmp = 0
        for j in range(diceCount):
            rolltmp = __randint(1,diceSides)
            rollStep.append(rolltmp)
            step = step + str(rolltmp)+','
        step = step[:-1]+'}['
        rollStep.sort(reverse = True)
        rollResult = 0
        for j in range(diceMax):
            step= step + str(rollStep[j])+'+'
            rollResult = rollResult + rollStep[j]
        step = step[:-1]+']('+str(rollResult)+')'
    elif diceMin != None:
        step = '{'
        rollStep = []
        rolltmp = 0
        for j in range(diceCount):
            rolltmp = __randint(1,diceSides)
            rollStep.append(rolltmp)
            step = step + str(rolltmp)+'+'
        step = step[:-1]+'}['
        rollStep.sort(reverse = False)
        rollResult = 0
        for j in range(diceMin):
            step= step + str(rollStep[j])+'+'
            rollResult = rollResult + rollStep[j]
        step = step[:-1]+']('+str(rollResult)+')'
    else:
        step = '{'
        rollStep= []
        for j in range(diceCount):
            rolltmp = __randint(1,diceSides)
            rollStep.append(rolltmp)
            step = step + str(rolltmp)+'+'
        step = step[:-1]+'}('
        rollResult = 0
        for j in rollStep:
            rollResult = rollResult + j
        step = step + str(rollResult)+')'
    return rollResult,step
# times 重复次数
# num 惩罚骰个数
def __dicePunish(times=1,num=1):
    # print(times,num)
    MaxDice = 9999
    if num == 0 or times == 0:
        raise (UserWarning('Zero_Dice_Error','投掷个数不能为0'))
    elif times > MaxDice or num > MaxDice:
        raise (UserWarning('Roll_Too_Big','投掷次数或单个面数过大'))
    if times == 1:
        rollStep = []
        ten = 0
        one = __randint(0,9)
        for j in range(num+1):
            rollStep.append(__randint(0,9))
            if rollStep[j] > ten :
                ten = rollStep[j]
            elif one == 0 and rollStep[j] == 0 :
                ten = 10
                rollStep[j] = 10
        rollFirst = 10 * rollStep.pop(0) + one
        rollResult = ten * 10 + one
        ROLL_List = ''
        for j in range(len(rollStep)):
            if rollStep[j] == ten:
                ROLL_List = ROLL_List +'<'+ str(rollStep[j])+'>,'
            else:
                ROLL_List = ROLL_List + str(rollStep[j])+','
        ROLL_List = ROLL_List[:-1]
        step = '{1D100 = '+str(rollFirst) +'惩罚骰:['+ROLL_List+']}('+str(rollResult)+')'
        return rollResult,step
    else:
        totalResult = 0
        totalStep = '{'
        for i in range(times):
            rollStep = []
            ten = 0
            one = __randint(0,9)
            for j in range(num+1):
                rollStep.append(__randint(0,9))
                if rollStep[j] > ten :
                    ten = rollStep[j]
                elif one == 0 and rollStep[j] == 0 :
                    ten = 10
                    rollStep[j] = 10
            rollFirst = 10 * rollStep.pop(0) + one
            rollResult = ten * 10 + one
            ROLL_List = ''
            for j in range(len(rollStep)):
                if rollStep[j] == ten:
                    ROLL_List = ROLL_List +'<'+ str(rollStep[j])+'>,'
                else:
                    ROLL_List = ROLL_List + str(rollStep[j])+','
            ROLL_List = ROLL_List[:-1]
            step = '{1D100 = '+str(rollFirst) +'惩罚骰:['+ROLL_List+']}('+str(rollResult)+')'
            totalResult = totalResult + rollResult
            totalStep = totalStep + step +'+'
        totalStep = totalStep[:-1]+'}('+str(totalResult)+')'
        return totalResult,totalStep
# times 重复次数
# num 奖励骰个数
def __diceBonus(times=1,num=1):
    # print(times,num)
    MaxDice = 9999
    if num == 0 or times == 0:
        raise (UserWarning('Zero_Dice_Error','投掷个数不能为0'))
    elif times > MaxDice or num > MaxDice:
        raise (UserWarning('Roll_Too_Big','投掷次数或单个面数过大'))
    if times == 1:
        rollStep = []
        ten = 10
        one = __randint(0,9)
        for j in range(num+1):
            rollStep.append(__randint(0,9))
            if one == 0 and rollStep[j] == 0 :
                ten = 10
                rollStep[j] = 10
            elif rollStep[j] < ten :
                ten = rollStep[j]
        rollFirst = rollStep.pop(0) * 10 + one
        rollResult = ten * 10 + one
        ROLL_List = ''
        for j in range(len(rollStep)):
            if rollStep[j] == ten:
                ROLL_List = ROLL_List +'<'+ str(rollStep[j])+'>,'
            else:
                ROLL_List = ROLL_List + str(rollStep[j])+','
        ROLL_List = ROLL_List[:-1]
        step = '{1D100 = '+str(rollFirst) +'奖励骰:['+ROLL_List+']}('+str(rollResult)+')'
        return rollResult,step
    else:
        totalResult = 0
        totalStep = '{'
        for i in range(times):
            rollStep = []
            ten = 10
            one = __randint(0,9)
            for j in range(num+1):
                rollStep.append(__randint(0,9))
                if one == 0 and rollStep[j] == 0 :
                    ten = 10
                    rollStep[j] = 10
                elif rollStep[j] < ten :
                    ten = rollStep[j]
            rollFirst = rollStep.pop(0) * 10 + one
            rollResult = ten * 10 + one
            ROLL_List = ''
            for j in range(len(rollStep)):
                if rollStep[j] == ten:
                    ROLL_List = ROLL_List +'<'+ str(rollStep[j])+'>,'
                else:
                    ROLL_List = ROLL_List + str(rollStep[j])+','
            ROLL_List = ROLL_List[:-1]
            step = '{1D100 = '+str(rollFirst) +'奖励骰:['+ROLL_List+']}('+str(rollResult)+')'
            totalResult = totalResult + rollResult
            totalStep = totalStep + step +'+'
        totalStep = totalStep[:-1]+'}('+str(totalResult)+')'
        return totalResult,totalStep
# 骰池
# AaBkCmD
# diceCount 个数(A)
# diceAdd 加骰线(B)
# dicesuccess 成功线(C)
# diceSides 面数(D)
def __dicePool(diceCount=1,diceAdd=10,diceSuccess=8,diceSides=10):
    # print(diceCount,diceAdd,diceSuccess,diceSides)
    diceMax = 9999
    if diceAdd > diceMax or diceCount > diceMax or diceSuccess > diceMax or diceSides > diceMax:
        raise (UserWarning('Roll_Too_Big','投掷次数或单个面数过大'))
    elif diceAdd == 0 or diceCount == 0 or diceSuccess == 0 or diceSides == 0:
        raise (UserWarning('Zero_Dice_Error','投掷个数不能为0'))
    thisPool = diceCount     # 当前骰池个数
    successCount = 0        # 成功个数
    step = ''
    while thisPool != 0:
        tmpPool = thisPool
        thisPool = 0
        step = step +'{'
        for i in range(tmpPool):
            roll = __randint(1,diceSides)
            if roll >= diceAdd:
                step = step +'<'
                thisPool = thisPool +1
                if roll >= diceSuccess:
                    successCount = successCount +1
                    step = step + '['+ str(roll) +']' +'>'
                else:
                    step = step + str(roll) + '>'
            elif roll >= diceSuccess:
                successCount = successCount + 1
                step = step + '['+ str(roll) +']'
            else:
                step = step + str(roll)
            step = step + ','
        step = step[:-1] + '}'
    step = step + '('+str(successCount)+')'
    return successCount , step



# 计算模块
def __RPNcal(cal):
    a = []
    x = 0
    y = 0

    tmp = None
    sign = {
        '+' : 1 , '-' : 1,
        '*' : 2 , '/' : 2,
        'd' : 3 , 'k':3, 'q':3,'p':3,'a':3,'m':3,'b':3  
    }
    # pointer = 0
    # while pointer < len(cal):
    #     tmp_tree = cal[pointer]
    for tmp_tree in cal:
        data = tmp_tree.data
        if type(data) == int:         # 数字
            a.append((data,str(data)))
        elif data == 'd':       # d
            vb,stepa = a.pop()
            va,stepa = a.pop()
            if tmp_tree.get_parent_data() in ('k','q') and tmp_tree.parent.left is tmp_tree:      # 父节点为修饰，且本身是其左节点
                a.append(('d','d'))
                a.append((va,'da'))
                a.append((vb,'db'))
            else:
                result,tmpstep = __diceRoll(diceCount=va,diceSides=vb)
                a.append((result,tmpstep))
        elif data == 'q':
            vc ,stepa = a.pop()
            vb ,stepa = a.pop()
            va ,stepa = a.pop()
            dd ,stepa = a.pop()
            if dd != 'd':
                raise(UserWarning('Roll_Exp_Invalid','投掷表达式不完整'))
            result,tmpstep = __diceRoll(diceCount=va,diceSides=vb,diceMin=vc)
            a.append((result,tmpstep))
        elif data == 'k':
            vc , stepa = a.pop()
            vb , stepa = a.pop()
            va , stepa = a.pop()
            dd , stepa = a.pop()
            if dd == 'd':
                result,tmpstep = __diceRoll(diceCount=va,diceSides=vb,diceMax=vc)
                a.append((result,tmpstep))
            elif dd == 'a':
                if tmp_tree.get_parent_data() == 'm' and tmp_tree.parent.left is tmp_tree:
                    a.append(('a','a'))
                    a.append((va,'pa'))
                    a.append((vb,'pb'))
                    a.append((vc,'pc'))
                else:
                    result,tmpstep = __dicePool(diceCount=va,diceAdd=vb,diceSuccess=vc)
                    a.append((result,tmpstep))
            else:
                raise(UserWarning('Roll_Exp_Invalid','投掷表达式不完整'))
        elif data == 'a':
            vb,stepa = a.pop()
            va,stepa = a.pop()
            if tmp_tree.get_parent_data() in ('k','m') and tmp_tree.parent.left is tmp_tree:
                a.append(('a','a'))
                a.append((va,'pa'))
                a.append((vb,'pb'))
            else:
                result,tmpstep = __dicePool(diceCount=va,diceAdd=vb)
                a.append((result,tmpstep))
        elif data == 'm':
            vd ,stepa = a.pop()
            vt , stepa = a.pop()
            vc = None
            if stepa == 'pc':
                vc = vt
                vb , stepa = a.pop()
                va , stepa = a.pop()
                dd , stepa = a.pop()
                if dd != 'a':
                    raise(UserWarning('Roll_Exp_Invalid','投掷表达式不完整'))
                result,tmpstep = __dicePool(diceCount=va,diceAdd=vb,diceSuccess=vc,diceSides=vd)
                a.append((result,tmpstep))
            elif stepa == 'pb':
                vb = vt
                va , stepa = a.pop()
                dd , stepa = a.pop()
                if dd != 'a':
                    raise(UserWarning('Roll_Exp_Invalid','投掷表达式不完整'))
                result,tmpstep = __dicePool(diceCount=va,diceAdd=vb,diceSides=vd)
                a.append((result,tmpstep))
            else:
                raise(UserWarning('Roll_Exp_Invalid','投掷表达式不完整'))
        elif data == 'p':
            vb ,stepb = a.pop()
            va ,stepa = a.pop()
            result,tmpstep = __dicePunish(times=va,num=vb)
            a.append((result,tmpstep))
        elif data == 'b':
            vb ,stepb = a.pop()
            va ,stepa = a.pop()
            result,tmpstep = __diceBonus(times=va,num=vb)
            a.append((result,tmpstep))
        ################################# 正常四则运算
        elif data == '+':
            vb , stepb = a.pop()
            va , stepa = a.pop()
            result = va + vb
            if sign.get(tmp_tree.left.data,10) < sign[data]:
                stepa = '('+stepa+')'
            if sign.get(tmp_tree.right.data,10) < sign[data]:
                stepb = '('+stepb+')'
            tmpstep = stepa + '+' + stepb
            a.append((result,tmpstep))
        elif data == '-':
            vb , stepb = a.pop()
            va , stepa = a.pop()
            result = va - vb
            if sign.get(tmp_tree.left.data,10) < sign[data]:
                stepa = '('+stepa+')'
            if sign.get(tmp_tree.right.data,10) <= sign[data]:
                stepb = '('+stepb+')'
            tmpstep = stepa + '-' + stepb
            a.append((result,tmpstep))
            # if tmp_tree.get_parent_data() == '+':
            #     tmpstep = stepa +'+'+ stepb
            # else :
            #     tmpstep = '('+stepa+'+'+stepb+')'
            # a.append(result,tmpstep)
        elif data == '*':
            vb , stepb = a.pop()
            va , stepa = a.pop()
            result = va * vb
            if sign.get(tmp_tree.left.data,10) < sign[data]:
                stepa = '('+stepa+')'
            if sign.get(tmp_tree.right.data,10) < sign[data]:
                stepb = '('+stepb+')'
            tmpstep = stepa + '*' + stepb
            a.append((result,tmpstep))
        elif data == '/':
            vb , stepb = a.pop()
            va , stepa = a.pop()
            result = va / vb
            if sign.get(tmp_tree.left.data,10) < sign[data]:
                stepa = '('+stepa+')'
            if sign.get(tmp_tree.right.data,10) <= sign[data]:
                stepb = '('+stepb+')'
            tmpstep = stepa + '/' + stepb
            a.append((result,tmpstep))
        else:
            break
    return a.pop()


def calculate(string:str,stepreturn = True):
    '''dice rd 运算模块， string 为运算表达式， 
    返回 (状态(T) , result (int) , step (str) )
    或 (状态(F) , '' , error_str )'''
    string = string.lower()
    try:
        splitdata = __split(string)
        # print(splitdata)
        cal = __RPNchange(splitdata)
        result , step = __RPNcal(cal)
        if stepreturn:
            return True,result ,step
        else:
            return result
    except UserWarning as err:
        a,b = err.args
        #print(a,b)
        if stepreturn:
            return False , a, b
        else:
            return None
    except Exception as err:
        if stepreturn:
            return False ,'', err.__str__()
        else:
            return None
# if __name__ == '__main__':
#     string = '3+100d1/01'
#     print(calculate(string))

