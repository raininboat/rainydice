# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  /
    /_/|_/_/ |_/___/_/|_/   /_/

    RainyDice 跑团投掷机器人服务 by RainyZhou
        ra 指令

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

from rainydice.dice_command import cal_btree
from rainydice.dice_command import coc7_constant as cons
from random import randint
from rainydice.cocRankCheckDefault import cocRankCheck as defaultRankCheck
import re

def callRA(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID):
    sign = 0
    refmt = '([bp]\d*)?(h)?\s*([^\d\s]*)\s*(\d*)\s*(\S*)'
    reobj = re.match(refmt,message)
    # ('p52', 'h', '测试', '93', '原因')
    if reobj == None:
        return -1,False,RainyDice.GlobalVal.GlobalMsg['InputErr']
    sign_str,isrh,skill_name,skill_val_str,reason=reobj.groups()
    if sign_str == None:
        sign_str = '1d100'
    if isrh != None and Group_ID != 0:
        isrh = True
    else:
        isrh = False
    if reason != '':
        reason = '由于'+reason+'，'
    if skill_val_str == '':
        card = RainyDice.user.get_card(platform=Group_Platform,user_id=User_ID)
        skill_name =  cons.name_replace(skill_name=skill_name)
        if skill_name in card['data']:
            skill_val = card['data'][skill_name]
        else:
            skill_val = cons.get_default_val(skill_name=skill_name)
    else:
        skill_val = int(skill_val_str)
    if Group_ID != 0:
        Group_Setcoc = RainyDice.group[Group_Platform][Group_ID]['Group_Setcoc']
    else :
        Group_Setcoc = 0
    rankName = RainyDice.GlobalVal.GlobalVal['rankName']
    user_name = RainyDice.user[Group_Platform][User_ID]['U_Name']

    status,result,step=cal_btree.calculate(sign_str)
    if not status:
        return -1,False,step

    rank = RaSuccess(total = result, skill_val= skill_val, setcoc= Group_Setcoc, cocRankCheck=RainyDice.cocRankCheck)
    # 'raReply' : '{reason}{User_Name}进行{Skill_Name}检定:\n{step} / {Skill_Val} {rank}',
    reply = RainyDice.GlobalVal.GlobalMsg['raReply']
    fmtdict = {
        'reason' : reason,
        'User_Name' : user_name,
        'Skill_Name' : skill_name,
        'sign' : sign_str,
        'result' : result,
        'step' : step,
        'Skill_Val' : skill_val,
        'rank' : rankName[rank]
    }
    reply = reply.format_map(fmtdict)
    if isrh:
        group_reply = RainyDice.GlobalVal.GlobalMsg['rhGroupReply']
        group_reply = str.format(group_reply,User_Name=user_name)#User_Name=user_name)
        # plugin_event.reply(group_reply)
        reply = '在['+RainyDice.group[Group_Platform][Group_ID]['Group_Name']+']('+str(Group_ID)+')中，'+reply
        # plugin_event.send('private',user_id,reply)
        return 2 , True , (('reply',group_reply),('send','private',User_ID,reply))
    else:
        return 1 , False , reply
# ----------------
# - 内部 api 实现 -
# ----------------

def RaSuccess(total,skill_val,setcoc=0,cocRankCheck:dict=None):
        if cocRankCheck == None:
            cocRankCheck = defaultRankCheck
        x = total
        y = skill_val
        if setcoc not in cocRankCheck:
            setcoc = 0
        if cocRankCheck[setcoc]['critical'](x,y):          # 大成功大失败判定默认版在 cocRankCheckDefault.py 中
            rank = 1    # 大成功                                # 具体载入的版本为 data/rainydice/conf/rankcheck.py
            return rank                                         # 对象位置在 RainyDice.cocRankCheck
        elif cocRankCheck[setcoc]['fumble'](x,y):
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