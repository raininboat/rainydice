# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  /
    /_/|_/_/ |_/___/_/|_/   /_/

    RainyDice 跑团投掷机器人服务 by RainyZhou
        投掷模块

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
import time
import re
from rainydice.diceClass import Dice
from rainydice.dice_command import coc7_constant as cons
from rainydice.dice_command.cal_btree import calculate
from random import randint
class rolldice(object):
    intdict = { '0' : 0, '1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9 }
    def __init__(self,cocRankCheck):
        self.cocRankCheck = cocRankCheck
        pass
    def _RaSuccess(self,total,skill_val,setcoc=0):
        x = total
        y = skill_val
        if setcoc not in self.cocRankCheck:
            setcoc = 0
        if self.cocRankCheck[setcoc]['critical'](x,y):          # 大成功大失败判定默认版在 cocRankCheckDefault.py 中
            rank = 1    # 大成功                                # 具体载入的版本为 data/rainydice/conf/rankcheck.py
            return rank                                         # 对象位置在 RainyDice.cocRankCheck
        elif self.cocRankCheck[setcoc]['fumble'](x,y):
            rank = 6    # 大失败
            return rank
        if x<= y/5 :
            rank = 2    # 极难成功
            return rank
        elif x <= y/2 :
            rank = 3    # 困难成功
            return rank
        elif x <= y :
            rank = 4    # 成功
            return rank
        elif x > y :
            rank = 5    # 失败
            return rank
        else:
            rank = 0    # 未知错误
            return rank

    def RD(Self,plugin_event,Proc,RainyDice,message:str,user_id:int,platform:int,group_id = 0):
        maxStepLen = 200
        message = str.strip(message)
        isRH=False
        if message.startswith('h'):
            isRH=True
            message=message[1:].strip()
        reobj = re.match('([\d\-\+\*/\(\)dkqpbma]*)(.*)',message,re.I)
        if reobj == None:
            reply = RainyDice.GlobalVal.GlobalMsg['InputErr'] +'\n'+message
            # plugin_event.reply(reply)
            return 1 , False , reply
        dice_exp , reason = reobj.groups()
        if dice_exp == '':
            dice_exp = '1d100'
        status,result,step = calculate(dice_exp)
        if status == False:
            return 1 , False , step
        user_name = RainyDice.user[platform][user_id]['U_Name']
        replace = {
            'User_Name' : user_name,
            'DiceExp' : dice_exp
        }
        # 超过最长的回复大小
        if len(step)<=maxStepLen:
            replace['DiceStep']=step+'='
            #reply = str.replace(reply,'[DiceStep]',step)
        else:
            replace['DiceStep']=''
            #reply = str.replace(reply,'[DiceStep]=','')
        replace['Result']=str(result)

        if isRH and group_id != 0:
            replace['Group_Name'] = RainyDice.group[platform][group_id]['Group_Name']
            replace['Group_ID'] = group_id
            rplgrp = RainyDice.GlobalVal.GlobalMsg['rhGroupReply'].format_map(replace)
            rplpvt = RainyDice.GlobalVal.GlobalMsg['rhPrivateReply'].format_map(replace)
            # 'rhGroupReply' : '{User_Name}进行了一次暗骰',
            # 'rhPrivateReply' : '在群聊[{Group_Name}]({Group_ID})中,{User_Name}进行投掷:\n{DiceExp}={DiceStep}{Result}',
            replypack = (('reply',rplgrp),('send','private',user_id,rplpvt))
            return 2,True,replypack
        else:
            reply = RainyDice.GlobalVal.GlobalMsg['rdReply']            # '[User_Name]进行投掷:\n[DiceExp]=[DiceStep]=[Result]',
            reply = str.format_map(reply,replace)
            # plugin_event.reply(reply)
            if reason != None and reason != '':
                reply = '由于'+reason +','+reply
            return 1 , False , reply
    def SC(self,plugin_event,Proc,RainyDice,message:str,user_id:int,platform:int,group_id = 0):
        if message.find('/') == -1:
            reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
            return -1 ,False, reply
        scExp = str.split(message,'/',1)

        card = RainyDice.user.get_card(platform=platform,user_id=user_id)
        # skill_name = '理智'
        # print(card['data'])
        if '理智' in card['data']:
            san = card['data']['理智']
        else:
            return -1 ,False,RainyDice.GlobalVal.GlobalMsg['scSanNull']
        if group_id != 0:
            Group_Setcoc = RainyDice.group[platform][group_id]['Group_Setcoc']
        else :
            Group_Setcoc = 0
        rankName = RainyDice.GlobalVal.GlobalVal['rankName']
        user_name = RainyDice.user[platform][user_id]['U_Name']#card['name']
        rollResult = randint(1,100)
        rank = self._RaSuccess(rollResult,san,Group_Setcoc)
        sanlose = 0
        reply = RainyDice.GlobalVal.GlobalMsg['scReply']
        replace = {
            'User_Name' : user_name,
            'Roll_Result' : str(rollResult),
            'Old_San' : str(san),
            'Rank' : rankName[rank],
        }
        if rollResult <= san:
            status,sanlose,step = calculate(scExp[0])
            if status ==False:
                return -1 ,False, step
            replace['San_Lose_Expression'] = scExp[0]
            # reply = str.replace(reply,'[San_Lose_Expression]',scExp[0])
        else:
            status,sanlose,step = calculate(scExp[1])
            if status ==False:
                return -1 ,False, step
            replace['San_Lose_Expression'] = scExp[1]
        nowSan = san - sanlose
        if nowSan <= 0 :
            nowSan = 0
        card['data']['理智'] = nowSan
        RainyDice.user.set_card(platform=platform,user_id=user_id,card_dict=card['data'],card_name=card['name'])
        # 'scReply' : '[User_Name]进行理智检定:\nD100 = [Roll_Result] / [Old_San] [Rank]\n理智损失: [San_Lose_Expression] = [San_Lose_Result] \n当前理智：[nowSan]',
        replace['San_Lose_Result'] = str(sanlose)
        replace['nowSan'] = str(nowSan)
        reply = str.format_map(reply,replace)
        return 1 ,False, reply
    def ST(self,plugin_event,Proc,RainyDice:Dice,message:str,user_id:int,platform:int,group_id = 0):
        st = []
        card = RainyDice.user.get_card(platform=platform,user_id=user_id)
        reply = ''
        if message.find('-') != -1:
            # st xxx +1
            st = message.split('-',1)
            st.append('-')
            reply = RainyDice.GlobalVal.GlobalMsg['stChangeReply']
            status,card,reply = self.__STChange(card=card,stChange=st,reply=reply)
            if status:
                RainyDice.user.set_card(platform=platform,user_id=user_id,card_dict=card['data'],card_name=card['name'])
                return 1,False,reply
            else:
                reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                return -1 ,False,reply
        elif message.find('+') != -1:
            st = message.split('+',1)
            st.append('+')
            reply = RainyDice.GlobalVal.GlobalMsg['stChangeReply']
            status,card,reply = self.__STChange(card=card,stChange=st,reply=reply)
            if status:
                RainyDice.user.set_card(platform=platform,user_id=user_id,card_dict=card['data'],card_name=card['name'])
                return 1,False,reply
            else:
                reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                return -1 ,False,reply
        elif message.find('?') != -1:
            st = message.split('?',1)
            reply = RainyDice.GlobalVal.GlobalMsg['stNewCardReply']
            card_name = st[0]
            card_id = RainyDice.user.new_card_id(platform=platform,user_id=user_id,card_name=card_name)
            # 'stNewCardReply' : '已记录[User_Name]的人物卡:\n[[Card_ID]][[Card_Name]]',
            status,card = self.__STCard(card_id=card_id,card_name=card_name,text = st[1])
            if status:
                user_name = RainyDice.user[platform][user_id]['U_Name']
                replace = {
                    'User_Name' : user_name,
                    'Card_ID' : str(card_id),
                    'Card_Name' : card_name
                }
                reply = str.format_map(reply,replace)
                RainyDice.user.set_card(platform=platform,user_id=user_id,card_dict=card['data'],card_name=card['name'],en_card = card_id)
                return 1, False,reply
            else:
                reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                return -1 ,False,reply
        elif message.startswith('del'):
            if message == 'del':
                reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                return -1 ,False,reply
            message = message[3:]
            # cons = Constant()
            skill_name = cons.name_replace(message)
            if skill_name == '':
                reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                return -1 ,False,reply
            if skill_name in card['data']:
                del card['data'][skill_name]
                RainyDice.user.set_card(platform=platform,user_id=user_id,card_dict=card['data'],card_name=card['name'])
            reply = RainyDice.GlobalVal.GlobalMsg['stDelReply']
            # 'stDelReply' : '已将[User_Name]的技能【[Skill_Name]】删除',
            replace = {
                'Card_Name' : card['name'],
                'Skill_Name' : skill_name
            }
            reply = str.format_map(replace,replace)
            return 1, False,reply
        elif message.startswith('name'):        # 修改人物卡名称
            if message == 'name':
                reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                return -1 ,False,reply
            message = str.strip(message[4:])
            reply = RainyDice.GlobalVal.GlobalMsg['stNameReply']
            user_name = RainyDice.user[platform][user_id]['U_Name']
            RainyDice.user.set('U_Name',message,platform=platform,user_id=user_id)
            replace = {
                    'User_Name' : user_name,
                    'Card_ID' : str(card['id']),
                    'Card_Name' : card['name'],
                    'New_Name' : message
                }
            reply = str.format_map(reply,replace)
            card['name'] = message
            RainyDice.user.set_card(platform=platform,user_id=user_id,card_dict=card['data'],card_name=card['name'])
            # 'stNameReply' : '已将[User_Name]的人物卡[[Card_ID]][[Card_Name]]名称改为：[New_Name]',
            return 1 ,False,reply
        elif message.startswith('clr'):
            RainyDice.user.del_card(platform=platform,user_id=user_id)
            reply = RainyDice.GlobalVal.GlobalMsg['stClrReply']
            # 'stClrReply' : '已将[Card_Name]的技能全部清除',
            reply = str.format(reply,Card_Name=card['name'])
            # reply = str.replace(reply,'[Card_Name]',card['name'])
            return 1, False,reply
        elif message.startswith('show'):
            user_name = RainyDice.user[platform][user_id]['U_Name']
            if message == 'show':
                data = card['data']
                text = ''
                for skill_name in data:
                    if skill_name == '_null':
                        continue
                    skill_val = data[skill_name]
                    text = text +skill_name+':'+str(skill_val) +'，'
                if text != '':
                    text = text[:-1]
                 # 'stShowAllReply' : '[User_Name]的人物卡[[Card_ID]][[Card_Name]]属性为：\n',
                reply = RainyDice.GlobalVal.GlobalMsg['stShowAllReply']
                replace = {
                    'User_Name' : user_name,
                    'Card_ID' : str(card['id']),
                    'Card_Name' : card['name'],
                }
                reply = str.format_map(reply,replace)
                reply = reply +  text
                return 1, False,reply
            else:
                skill_name = message[4:]
                # cons = Constant()
                skill_name =cons.name_replace(skill_name)
                if skill_name in card['data']:
                    skill_val = card['data'][skill_name]
                else:
                    skill_val = cons.get_default_val(skill_name)
                reply = RainyDice.GlobalVal.GlobalMsg['stShowReply']
                replace = {
                    'User_Name' : user_name,
                    'Card_ID' : str(card['id']),
                    'Card_Name' : card['name'],
                    'Skill_Name' : skill_name,
                    'Skill_Val' : str(skill_val),
                }
                reply = str.format_map(reply,replace)

                return 1, False,reply
                # 'stShowReply' : '[User_Name]的人物卡[[Card_ID]][[Card_Name]]中属性【[Skill_Name]】为：[Skill_Val]',
        else:
            reply = RainyDice.GlobalVal.GlobalMsg['stSetReply']
            status,card_new = self.__STCard(card_id=card['id'],card_name=card['name'],text=message)
            if status:
                #print(card)
                card['data'].update(card_new['data'])
                #print(card)
                user_name = RainyDice.user[platform][user_id]['U_Name']
                RainyDice.user.set_card(platform=platform,user_id=user_id,card_dict=card['data'],card_name=card['name'])
                return 1, False,reply
            else:
                reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                return -1 ,False,reply
    def __STCard(self,card_id,card_name,text):
        card_data = {}
        text = str.strip(text)
        # cons = Constant()
        while text != '':
            reobj = re.match('(\D+)(\d+)',text)
            if reobj == None:
                break
            skill_name,skill_val_str = reobj.groups()
            skill_name = skill_name.replace(' ','')
            skill_name =cons.name_replace(skill_name)
            skill_val = int(skill_val_str)
            if skill_name != '':
                card_data[skill_name] = skill_val
            text = str.lstrip(text[reobj.span()[1]:])
        card = {
            'id' : card_id,
            'name' : card_name,
            'data' : card_data
        }

        if card_data == {}:
            return False , {}
        else:
            return True , card

    def __STChange(self,card,stChange,reply):
        # 'stChangeReply' : '已记录[User_Name]的属性变化:\n[Skill_Name]：[Skill_Val][Change_Expression]=[Skill_Val][Change_Result]=[Skill_Val_Result]',
        # cons = Constant()
        skill_name =  cons.name_replace(skill_name=stChange[0])
        changeExp = stChange[1]
        skill_val = 0
        if skill_name in card['data']:
            skill_val = card['data'][skill_name]
        else:
            skill_val = cons.get_default_val(skill_name=skill_name)
        if stChange[2] == '+':
            status,change_result,step = calculate(changeExp)
            if status == False:
                return False , {} , ''
            skill_changed = skill_val + change_result
            changeExp = ' + '+changeExp
            change_result_str = ' + '+str(change_result)
        elif stChange[2] == '-':
            status,change_result,step = calculate(changeExp)
            if status == False:
                return False , {} , ''
            skill_changed = skill_val - change_result
            changeExp = ' - '+changeExp
            change_result_str = ' - '+str(change_result)
        if skill_changed <= 0:      # 技能值非负
            skill_changed = 0
        card['data'][skill_name] = skill_changed
        replace = {
            'User_Name' : card['name'],
            'Skill_Name' : skill_name,
            'Skill_Val' : str(skill_val),
            'Change_Expression' : changeExp,
            'Change_Result' : change_result_str,
            'Skill_Val_Result' : str(skill_changed)
        }
        reply = str.format_map(reply,replace)
        return True , card , reply

    def LI(self,plugin_event,Proc,RainyDice,message:str,user_id:int,platform:int,group_id = 0):
        status = randint(0,9)
        user_name = RainyDice.user[platform][user_id]['U_Name']
        text = user_name+'疯狂发作-总结症状：\n1D10='+str(status+1)+'\n'+cons.LongInsanity[status]
        temp = randint(0,9)
        var_a = '1D10=' + str(temp+1)
        if  status == 8 :
            temp = randint(0,99)
            var_b = "1D100="+str(temp+1)
            var_c = cons.strFear[temp]
            text = str.format(text,var_a,var_b,var_c)
        elif status == 9:
            temp = randint(0,99)
            var_b = "1D100="+str(temp+1)
            #text = text.replace("[var_b]",addTxt)
            var_c = cons.strPanic[temp]
            text = str.format(text,var_a,var_b,var_c)
        else:
            text = str.format(text,var_a)
        return 1,False , text

    def TI(self,plugin_event,Proc,RainyDice,message:str,user_id:int,platform:int,group_id = 0):
        status = randint(0,9)
        user_name = RainyDice.user[platform][user_id]['U_Name']
        text = user_name+'疯狂发作-临时症状：\n1D10='+str(status+1)+'\n'+cons.TempInsanity[status]
        temp = randint(0,9)
        var_a = '1D10=' + str(temp+1)
        if  status == 8 :
            temp = randint(0,99)
            var_b = "1D100="+str(temp+1)
            var_c = cons.strFear[temp]
            text = str.format(text,var_a,var_b,var_c)
        elif status == 9:
            temp = randint(0,99)
            var_b = "1D100="+str(temp+1)
            var_c = cons.strPanic[temp]
            text = str.format(text,var_a,var_b,var_c)
        else:
            text = str.format(text,var_a)
        return 1,False,text
    def SETCOC(self,plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID = 0):
        if str.isdecimal(message):
            Group_Setcoc = self.intdict[message]
            # if Group_Setcoc > 5:
            #     reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
            #     return -1 ,False,reply
            if Group_ID != 0:
                status = RainyDice.group.set('Group_Setcoc',Group_Setcoc,Group_Platform,Group_ID)
                if status == False:
                    reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                    return -1 ,False,reply
                reply = RainyDice.GlobalVal.GlobalMsg['setcocReply']
                #'Group_SetcocReply' : '群聊房规属性已改为[Group_Setcoc]:\n[Group_SetcocExplain]'
                setcocExplain = RainyDice.GlobalVal.GlobalVal['setcocExplain'][Group_Setcoc]
                replace = {
                    'setcoc' : str(Group_Setcoc),
                    'setcocExplain' : setcocExplain
                }
                reply = str.format_map(reply,replace)
                return 1 ,False,reply
            else :
                reply = RainyDice.GlobalVal.GlobalMsg['OnlyInGroup']
                return -1 ,False,reply
        else :
            reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
            return -1 ,False,reply
    def EN(self,plugin_event,Proc,RainyDice,message:str,user_id:int,platform:int,group_id = 0):
        # cons = Constant()
        card = RainyDice.user.get_card(platform=platform,user_id=user_id)
        reply = ''
        name = card['name']
        skill_val = 0
        if '+' in message:
            # .en xxx +1D6
            tmplist = message.split('+',1)
            skill_name = tmplist[0].strip()
            skill_name =  cons.name_replace(skill_name=skill_name)
            exp = tmplist[1].strip()
            if exp == '':
                exp = '1D10'
            if skill_name in card['data']:
                skill_val = card['data'][skill_name]
            else:
                skill_val = cons.get_default_val(skill_name=skill_name)
        else:
            # .en xxx (30)
            match = re.match('(\D+)\s*(\d*)',message)
            if match == None:
                reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                return -1 ,False,reply
            skill_name,skill_val_str = match.groups()
            skill_name =  cons.name_replace(skill_name=skill_name.strip())
            if skill_val_str == '':
                if skill_name in card['data']:
                    skill_val = card['data'][skill_name]
                else:
                    skill_val = cons.get_default_val(skill_name=skill_name)
            else:
                skill_val = int(skill_val_str)
            exp = '1d10'
        roll = randint(1,100)
        if roll > skill_val or roll > 95 :
            # 'enReplySuccess' : '[User_Name]进行[Skill_Name]增长检定:\nD100 = [Roll]/[Old_Skill] 成功！\n[Skill_Name]:[Old_Skill]+[En_Exp]=[Old_Skill]+[En_Step]=[Now_Skill]',
            reply = RainyDice.GlobalVal.GlobalMsg['enReplySuccess']
            status = True
        else:
            # 'enReplyFail' : '[User_Name]进行[Skill_Name]增长检定:\nD100 = [Roll]/[Old_Skill] 失败！',
            reply = RainyDice.GlobalVal.GlobalMsg['enReplyFail']
            status = False
        if status:
            status,result,step = calculate(exp)
            if not status:
                reply = RainyDice.GlobalVal.GlobalMsg['InputErr']+step
                return 1 ,False,reply
            skill_val_new = skill_val + result
            card['data'][skill_name]=skill_val_new
            RainyDice.user.set_card(platform=platform,user_id=user_id,card_dict=card['data'],card_name=name)
            replace = {
                'User_Name' : name,
                'Skill_Name' : skill_name,
                'Roll' : str(roll),
                'Old_Skill' : str(skill_val),
                'En_Exp' : exp,
                'En_Step' : step,
                'Now_Skill' : str(skill_val_new)
            }
            reply = str.format_map(reply,replace)
            return 1 ,False,reply
        else:
            replace = {
                'User_Name' : name,
                'Skill_Name' : skill_name,
                'Roll' : str(roll),
                'Old_Skill' : str(skill_val)
            }
            reply = str.format_map(reply,replace)
            return 2 ,False,reply

    def RECALL(self,plugin_event,Proc,RainyDice:Dice,message:str,user_id:int,platform:int,group_id = 0):
        if message.startswith('on'):
            RainyDice.group.set('isBanRecall',True,platform,group_id)
            reply= '已开启消息撤回阻止'
            return 0,False,reply
        elif message.startswith('off'):
            RainyDice.group.set('isBanRecall',False,platform,group_id)
            reply= '已关闭消息撤回阻止'
            return 0,False,reply

