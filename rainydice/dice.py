# -*- coding: utf-8 -*-
'''
   ___  ___   _____  ____  __
  / _ \/ _ | /  _/ |/ /\ \/ /
 / , _/ __ |_/ //    /  \  / 
/_/|_/_/ |_/___/_/|_/   /_/  
                             
    测试内容

'''
import re
from rainydice.diceClass import Dice
from rainydice.constant import Constant
from rainydice.cal_btree import calculate
from random import randint
class rolldice(object):
    intdict = { '0' : 0, '1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9 }
    def __init__(self,cocRankCheck):
        self.cocRankCheck = cocRankCheck
        pass
    def _RaSuccess(self,total,skill_val,setcoc=0):
        mode = setcoc
        x = total
        y = skill_val
        if setcoc not in self.cocRankCheck:
            setcoc = 0
        if self.cocRankCheck[setcoc]['critical'](x,y):
            rank = 1    # 大成功
            return rank
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
    def RA(self,plugin_event,Proc,RainyDice,message:str,user_id,platform,group_id = 0):
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
            setcoc = 0
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
            successLevel = self._RaSuccess(rollResult,skill_val,setcoc)
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
            successLevel = self._RaSuccess(rollResult,skill_val,setcoc)
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
    def RD(Self,plugin_event,Proc,RainyDice,message:str,user_id:int,platform:int,group_id = 0):
        maxStepLen = 200
        message = str.strip(message)
        reobj = re.match('([\d\-\+\*/\(\)dD]+)(.*)',message,re.I)
        if reobj == None:
            reply = RainyDice.GlobalVal.GlobalMsg['InputErr'] +'\n'+message
            # plugin_event.reply(reply)
            return 1 , False , reply
        dice_exp , reason = reobj.groups()
        status,result,step = calculate(dice_exp)
        if status == False:
            return 1 , False , step
        user_name = RainyDice.user[platform][user_id]['U_Name']
        reply = RainyDice.GlobalVal.GlobalMsg['rdReply']            # '[User_Name]进行投掷:\n[DiceExp]=[DiceStep]=[Result]',
        reply = str.replace(reply,'[User_Name]',user_name)
        reply = str.replace(reply,'[DiceExp]',dice_exp)
        if len(step)<=maxStepLen:
            reply = str.replace(reply,'[DiceStep]',step)
        else:
            reply = str.replace(reply,'[DiceStep]=','')
        reply = str.replace(reply,'[Result]',str(result))
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
            setcoc = RainyDice.group[platform][group_id]['setcoc']
        else :
            setcoc = 0
        rankName = RainyDice.GlobalVal.GlobalVal['rankName']
        user_name = RainyDice.user[platform][user_id]['U_Name']#card['name']
        rollResult = randint(1,100)
        sanlose = 0
        reply = RainyDice.GlobalVal.GlobalMsg['scReply']
        if rollResult <= san:
            status,sanlose,step = calculate(scExp[0])
            if status ==False:
                return -1 ,False, step
            reply = str.replace(reply,'[San_Lose_Expression]',scExp[0])
        else:
            status,sanlose,step = calculate(scExp[0])
            if status ==False:
                return -1 ,False, step
            reply = str.replace(reply,'[San_Lose_Expression]',scExp[1])
        rank = self._RaSuccess(rollResult,san,setcoc)
        nowSan = san - sanlose
        if nowSan <= 0 :
            nowSan = 0
        card['data']['理智'] = nowSan
        RainyDice.user.set_card(platform=platform,user_id=user_id,card_dict=card['data'],card_name=card['name'])
        # 'scReply' : '[User_Name]进行理智检定:\nD100 = [Roll_Result] / [Old_San] [Rank]\n理智损失: [San_Lose_Expression] = [San_Lose_Result] \n当前理智：[nowSan]',
        reply = str.replace(reply,'[User_Name]',user_name)
        reply = str.replace(reply,'[Roll_Result]',str(rollResult))
        reply = str.replace(reply,'[Old_San]',str(san))  
        reply = str.replace(reply,'[Rank]',rankName[rank])
        reply = str.replace(reply,'[San_Lose_Result]',str(sanlose))
        reply = str.replace(reply,'[nowSan]',str(nowSan))
        return 1 ,False, reply
    def ST(self,plugin_event,Proc,RainyDice,message:str,user_id:int,platform:int,group_id = 0):
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
            status,card = self.__STCard(card_id=card_id,card_name=card_name,text = st[1],reply=reply)
            if status:
                user_name = RainyDice.user[platform][user_id]['U_Name']
                reply = str.replace(reply,'[User_Name]',user_name)
                reply = str.replace(reply,'[Card_ID]',str(card_id))
                reply = str.replace(reply,'[Card_Name]',card_name)
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
            cons = Constant()
            skill_name = cons.name_replace(message)
            if skill_name == '':
                reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                return -1 ,False,reply
            if skill_name in card['data']:
                del card['data'][skill_name]
                RainyDice.user.set_card(platform=platform,user_id=user_id,card_dict=card['data'],card_name=card['name'])
            reply = RainyDice.GlobalVal.GlobalMsg['stDelReply']
            # 'stDelReply' : '已将[User_Name]的技能【[Skill_Name]】删除',
            reply = str.replace(reply,'[Card_Name]',card['name'])
            reply = str.replace(reply,'[Skill_Name]',skill_name)
            return 1, False,reply
        elif message.startswith('name'):        # 修改人物卡名称
            if message == 'name':
                reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                return -1 ,False,reply
            message = str.strip(message[4:])
            reply = RainyDice.GlobalVal.GlobalMsg['stNameReply']
            user_name = RainyDice.user[platform][user_id]['U_Name']
            reply = str.replace(reply,'[User_Name]',user_name)
            reply = str.replace(reply,'[Card_ID]',str(card['id']))
            reply = str.replace(reply,'[Card_Name]',card['name'])
            reply = str.replace(reply,'[New_Name]',message)
            card['name'] = message
            RainyDice.user.set_card(platform=platform,user_id=user_id,card_dict=card['data'],card_name=card['name'])
            # 'stNameReply' : '已将[User_Name]的人物卡[[Card_ID]][[Card_Name]]名称改为：[New_Name]',
            return 1 ,False,reply
        elif message.startswith('clr'):
            RainyDice.user.del_card(platform=platform,user_id=user_id,)
            reply = RainyDice.GlobalVal.GlobalMsg['stClrReply']
            # 'stClrReply' : '已将[Card_Name]的技能全部清除',
            reply = str.replace(reply,'[Card_Name]',card['name'])
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
                reply = str.replace(reply,'[User_Name]',user_name)
                reply = str.replace(reply,'[Card_ID]',str(card['id']))
                reply = str.replace(reply,'[Card_Name]',card['name'])
                reply = reply +  text
                return 1, False,reply
            else:
                skill_name = message[4:]
                cons = Constant()
                skill_name =cons.name_replace(skill_name)
                if skill_name in card['data']:
                    skill_val = card['data'][skill_name]
                else:
                    skill_val = cons.get_default_val(skill_name)
                reply = RainyDice.GlobalVal.GlobalMsg['stShowReply']
                reply = str.replace(reply,'[User_Name]',user_name)
                reply = str.replace(reply,'[Card_ID]',str(card['id']))
                reply = str.replace(reply,'[Card_Name]',card['name'])
                reply = str.replace(reply,'[Skill_Name]',skill_name)
                reply = str.replace(reply,'[Skill_Val]',str(skill_val))
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
        cons = Constant()
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
        cons = Constant()
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
        reply = str.replace(reply,'[User_Name]',card['name'])
        reply = str.replace(reply,'[Skill_Name]',skill_name)
        reply = str.replace(reply,'[Skill_Val]',str(skill_val))  
        reply = str.replace(reply,'[Change_Expression]',changeExp)
        reply = str.replace(reply,'[Change_Result]',change_result_str)
        reply = str.replace(reply,'[Skill_Val_Result]',str(skill_changed))            
        return True , card , reply

    def LI(self):
        status = randint(0,9)
        text = '{nick}疯狂发作-总结症状：\n1D10='+str(status+1)+'\n'+Constant.LongInsanity[status]
        temp = randint(0,9)
        addTxt = '1D10=' + str(temp+1)
        text = text.replace('[var_a]',addTxt)
        if  status == 8 :
            temp = randint(0,99)
            addTxt = "1D100="+str(temp+1)
            text = text.replace("[var_b]",addTxt)
            addTxt = Constant.strFear[temp]
            text = text.replace("[var_c]",addTxt)
        elif status == 9:
            temp = randint(0,99)
            addTxt = "1D100="+str(temp+1)
            text = text.replace("[var_b]",addTxt)
            addTxt = Constant.strPanic[temp]
            text = text.replace("[var_c]",addTxt)           
        return 1,False , text

    def TI(self):
        status = randint(0,9)
        text = '{nick}疯狂发作-临时症状：\n1D10='+str(status+1)+'\n'+Constant.TempInsanity[status]
        temp = randint(0,9)
        addTxt = '1D10=' + str(temp+1)
        text = text.replace("[var_a]",addTxt)
        if  status == 8 :
            temp = randint(0,99)
            addTxt = "1D100="+str(temp+1)
            text = text.replace("[var_b]",addTxt)
            addTxt = Constant.strFear[temp]
            text = text.replace("[var_c]",addTxt)
        elif status == 9:
            temp = randint(0,99)
            addTxt = "1D100="+str(temp+1)
            text = text.replace("[var_b]",addTxt)
            addTxt = Constant.strPanic[temp]
            text = text.replace("[var_c]",addTxt)
        return 1,False,text
    def SETCOC(self,plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID = 0):
        if message in self.intdict:
            setcoc = self.intdict[message]
            if setcoc > 5:
                reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                return -1 ,False,reply
            if Group_ID != 0:
                status = RainyDice.group.set('setcoc',[setcoc],Group_Platform,Group_ID)
                if status == False:
                    reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
                    return -1 ,False,reply
                reply = RainyDice.GlobalVal.GlobalMsg['setcocReply']
                #'setcocReply' : '群聊房规属性已改为[setcoc]:\n[setcocExplain]'
                setcocExplain = RainyDice.GlobalVal.GlobalVal['setcocExplain'][setcoc]
                reply = str.replace(reply,'[setcoc]',str(setcoc))
                reply = str.replace(reply,'[setcocExplain]',setcocExplain)
                return 1 ,False,reply
            else :
                reply = RainyDice.GlobalVal.GlobalMsg['OnlyInGroup']
                return -1 ,False,reply
        else :
            reply = RainyDice.GlobalVal.GlobalMsg['InputErr']
            return -1 ,False,reply
    def EN(self,plugin_event,Proc,RainyDice:Dice,message:str,user_id:int,platform:int,group_id = 0):
        
        pass
