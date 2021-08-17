
# -*- coding: utf-8 -*-
'''
   ___  ___   _____  ____  __
  / _ \/ _ | /  _/ |/ /\ \/ /
 / , _/ __ |_/ //    /  \  / 
/_/|_/_/ |_/___/_/|_/   /_/  
                             
    测试内容

'''
import rainydice
import re
from rainydice.constant import Constant
from rainydice.calculate import RPN
from random import randint
class rolldice(object):
    intdict = { '0' : 0, '1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9 }
    def _RaSuccess(self,total,val,setcoc=[1,0,1,0,96,0,100,0,50]):
        i = setcoc[8]
        x = total
        y = val
        if ((x < i) and (x <= setcoc[0]+setcoc[1])*val) or ((y >= i) and (x <= setcoc[2]+val*(setcoc[3]))):
            rank = 1    # 大成功
        elif ((y < i) and (x >= setcoc[4]+setcoc[5])*val) or ((y >= i) and (x >= setcoc[6]+val*(setcoc[7]))):
            rank = 6    # 大失败
        elif x<= y/5 :
            rank = 2    # 极难成功
        elif x <= y/2 :
            rank = 3    # 困难成功
        elif x <= y :
            rank = 4    # 成功
        elif x > y :
            rank = 5    # 失败
        else:
            rank = 0
        return rank
    def _rd(self,sign):
        if sign == 0 :
            rollResult = randint(1,100)
            rollStep = [rollResult]
            rollFirst = rollResult
        elif sign < 0 :
            rollStep = []
            ten = 0
            one = randint(0,9)
            sign = -sign
            for i in range(sign+1):
                rollStep.append(randint(0,9))
                if rollStep[i] > ten :
                    ten = rollStep[i]
                elif one == 0 and rollStep[i] == 0 :
                    ten = 10
                    rollStep[i] = 10
            rollFirst = 10 * rollStep.pop(0) + one
            rollResult = ten * 10 + one
        elif sign > 0 :
            rollStep = []
            ten = 10
            one = randint(0,9)
            for i in range(sign+1):
                rollStep.append(randint(0,9))
                if one == 0 and rollStep[i] == 0 :
                    ten = 10
                    rollStep[i] = 10
                elif rollStep[i] < ten :
                    ten = rollStep[i]
            rollFirst = rollStep.pop(0) * 10 + one
            rollResult = ten * 10 + one
        return rollResult,rollStep,rollFirst
    def __change_rollstep_to_str(self,rollstep):
        ROLL_List = ''
        for i in range(len(rollstep)):
            ROLL_List = ROLL_List + str(rollstep[i])+','
        ROLL_List = ROLL_List[:-1]
        return ROLL_List
    def RA(self,plugin_event,Proc,RainyDice:rainydice.rainydice.diceClass.Dice,message:str,user_id,platform,group_id = 0):
        sign = 0
        message = message +'     '
        if message.startswith('b'):
            sign = 1
            if message[1] in self.intdict:
                sign = self.intdict[message[1]]
                if sign == 0 :
                    return -1,False,RainyDice.GlobalVal.GlobalMsg['InputErr']
                if message[2] in self.intdict:
                    reply =RainyDice.GlobalVal.GlobalMsg['InputErr']+'\n 奖励骰数量过多'
                    return -2,False,reply
                message = message[2:]
            message = message[1:]
        elif message.startswith('p'):
            sign = -1
            if message[1] in self.intdict:
                sign = -self.intdict[message[1]]
                if sign == 0 :
                    reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                    return -1 ,False, reply
                if message[2] in self.intdict:
                    reply = RainyDice.GlobalVal.GlobalMsg['InputErr']+'\n 惩罚骰数量过多'
                    return -2 , False, reply
                message = message[2:]
            message = message[1:]
        if message.startswith('h'):                 # 暗骰
            if group_id != 0:
                isRH = True
                message=message[1:]
        else:
            isRH = False
        if message.isspace():       # 则指令只包含前缀部分
            rollResult,rollStep,rollFirst = self._rd(sign)

        message.lstrip()
        skill_val_str = ''
        skill_name = ''
        temp_re_obj = re.match('(\d+)',message)     # .ra (34) xxx
        if temp_re_obj != None:
            span = temp_re_obj.span()
            match = temp_re_obj.group()
            skill_val = int(match)
            if span[1] < len(message):
                skill_name = message[span[1]:]
        else:
            temp_re_obj = re.match('(\D+)',message)     # .ra (xxx) 34
            if temp_re_obj != None:
                span = temp_re_obj.span()
                match = temp_re_obj.group()
                skill_name = match
                if span[1] < len(message):
                    message = str.lstrip(message[span[1]:])
                    skill_val_str = re.match('(\d+)?',message).group()
            else:
                reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                return -3 , False , reply
        cons = Constant()
        if skill_val_str == '':
            card = RainyDice.user.get_card(platform=platform,user_id=user_id)
            skill_name =  cons.name_replace(skill_name=skill_name)
            if skill_name in card['data']:
                skill_val = card['data'][skill_name]
            else:
                skill_val = cons.get_default_val(skill_name=skill_name)
        else:
            skill_val = int(skill_val_str)
        if group_id != 0:
            setcoc = RainyDice.group[platform][group_id]['setcoc']
        else :
            setcoc = [1,0,1,0,96,0,100,0,50]
        rankName = RainyDice.GlobalVal.GlobalVal['rankName']
        user_name = RainyDice.user[platform][user_id]['U_Name']#card['name']
        # print('sign : '+str(sign))
        # print('skill_name : '+skill_name)
        # print('skill_val : '+str(skill_val))
        if sign == 0 :
            reply = RainyDice.GlobalVal.GlobalMsg['raReply']    # '[User_Name]进行[Skill_Name]检定:\nD100 = [Result] / [Skill_Val] [Rank]',
            rollResult = randint(1,100)
            successLevel = self._RaSuccess(rollResult,skill_val,setcoc)
            reply = str.replace(reply,'[User_Name]',user_name)
            reply = str.replace(reply,'[Skill_Name]',skill_name)
            reply = str.replace(reply,'[Result]',str(rollResult))
            reply = str.replace(reply,'[Skill_Val]',str(skill_val))
            reply = str.replace(reply,'[Rank]',rankName[successLevel])
        elif sign < 0 :
            rollResult,rollStep,rollFirst = self._rd(sign)
            successLevel = self._RaSuccess(rollResult,skill_val)
            ROLL_List = self.__change_rollstep_to_str(rollstep=rollStep)
            reply = RainyDice.GlobalVal.GlobalMsg['rbpReply']    #  '[User_Name]进行[Skill_Name]检定:\nD100 = [Result] [[Sign]骰:[ROLL_List]] / [Skill_Val] [Rank]',
            reply = str.replace(reply,'[User_Name]',user_name)
            reply = str.replace(reply,'[Skill_Name]',skill_name)
            reply = str.replace(reply,'[rdResult]',str(rollFirst))
            reply = str.replace(reply,'[Result]',str(rollResult))
            reply = str.replace(reply,'[Sign]','惩罚')
            reply = str.replace(reply,'[ROLL_List]',ROLL_List)
            reply = str.replace(reply,'[Skill_Val]',str(skill_val))
            reply = str.replace(reply,'[Rank]',rankName[successLevel])
        elif sign > 0 :
            rollResult,rollStep,rollFirst = self._rd(sign)
            successLevel = self._RaSuccess(rollResult,skill_val)
            ROLL_List = self.__change_rollstep_to_str(rollstep=rollStep)
            reply = RainyDice.GlobalVal.GlobalMsg['rbpReply']    #  '[User_Name]进行[Skill_Name]检定:\nD100 = [Result] [[Sign]骰:[ROLL_List]] / [Skill_Val] [Rank]',
            reply = str.replace(reply,'[User_Name]',user_name)
            reply = str.replace(reply,'[Skill_Name]',skill_name)
            reply = str.replace(reply,'[rdResult]',str(rollFirst))
            reply = str.replace(reply,'[Result]',str(rollResult))
            reply = str.replace(reply,'[Sign]','奖励')
            reply = str.replace(reply,'[ROLL_List]',ROLL_List)
            reply = str.replace(reply,'[Skill_Val]',str(skill_val))
            reply = str.replace(reply,'[Rank]',rankName[successLevel])
            
        if isRH:
            group_reply = RainyDice.GlobalVal.GlobalMsg['rhGroupReply']
            group_reply = str.replace(group_reply,'[User_Name]',user_name)
            # plugin_event.reply(group_reply)
            reply = '在['+RainyDice.group[platform][group_id]['Group_Name']+']('+str(group_id)+')中，'+reply
            # plugin_event.send('private',user_id,reply)
            return 2 , True , (('reply',group_reply),('send','private',user_id,reply))
        else:
            return 1 , False , reply
    def RD(Self,plugin_event,Proc,RainyDice:rainydice.rainydice.diceClass.Dice,message:str,user_id:int,platform:int,group_id = 0):
        cal = RPN()
        message = str.strip(message)
        reobj = re.match('([\d\-\+\*/\(\)dD]+)(.*)',message,re.I)
        if reobj == None:
            reply = RainyDice.GlobalVal.GlobalMsg['InputErr'] +'\n'+message
            # plugin_event.reply(reply)
            return 1 , False , reply
        try:
            dice_exp , reason = reobj.groups()
            result = cal.calculate(dice_exp)
            user_name = RainyDice.user[platform][user_id]['U_Name']
            reply = RainyDice.GlobalVal.GlobalMsg['rdReply']            # '[User_Name]进行投掷:\n[DiceExp]=[Result]',
            reply = str.replace(reply,'[User_Name]',user_name)
            reply = str.replace(reply,'[DiceExp]',dice_exp)
            reply = str.replace(reply,'[Result]',str(result))
            # plugin_event.reply(reply)
            if reason != None and reason != '':
                reply = '由于'+reason +','+reply
            return 1 , False , reply
        except:
            reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
            # plugin_event.reply(reply)
            return 1 , False , reply
    def _rbp(self,plugin_event,Proc,RainyDice:rainydice.rainydice.diceClass.Dice,message:str,user_id:int,platform:int,group_id = 0):
        sign = 0
        if message.startswith('b'):
            sign = 1
            if message[1] in self.intdict:
                sign = self.intdict[message[1]]
                if sign == 0 :
                    return -1,False,RainyDice.GlobalVal.GlobalMsg['InputErr']
                if message[2] in self.intdict:
                    reply =RainyDice.GlobalVal.GlobalMsg['InputErr']+'\n 奖励骰数量过多'
                    return -2,False,reply
        elif message.startswith('p'):
            sign = -1
            if message[1] in self.intdict:
                sign = -self.intdict[message[1]]
                if sign == 0 :
                    reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                    return -1 ,False, reply
                if message[2] in self.intdict:
                    reply = RainyDice.GlobalVal.GlobalMsg['InputErr']+'\n 惩罚骰数量过多'
                    return -2 , False, reply
        rollResult,rollStep,rollFirst = self._rd(sign)
        ROLL_List = self.__change_rollstep_to_str(rollstep=rollStep)

        