# -*- coding: utf-8 -*-
'''
   ___  ___   _____  ____  __
  / _ \/ _ | /  _/ |/ /\ \/ /
 / , _/ __ |_/ //    /  \  /
/_/|_/_/ |_/___/_/|_/   /_/

    coc新卡做成

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
import re
from rainydice.dice_command import cal_btree
from rainydice.dice_command import coc7_constant
from rainydice.dice_command import message_send

COC7_CARD_SHORT_TAMPLATE = '''\
力量:{str}, 敏捷:{dex}, 意志:{pow},
体质:{con}, 外貌:{app}, 教育:{edu},
体型:{siz}, 智力:{int}, 幸运:{luck},
总计: {total_without_luck} / {total_with_luck}\
'''
COC7_CARD_DETAIL_TAMPLATE = '''\
力量:3D6*5={str_step}={str}
体质:3D6*5={con_step}={con}
体型:2D6*5+30={siz_step}={siz}
敏捷:3D6*5={dex_step}={dex}
外貌:3D6*5={app_step}={app}
智力:2D6*5+30={int_step}={int}
意志:3D6*5={pow_step}={pow}
教育:2D6*5+30={edu_step}={edu}
幸运:3D6*5={luck_step}={luck}
总计: {total_without_luck} / {total_with_luck}
生命值:{hp}, 魔法值:{mp}, 理智值:{pow}
伤害价值:{DB}, 体格:{Build}\
'''
COC6_CARD_SHORT_TAMPLATE = '''\
力量:{str}, 敏捷:{dex}, 意志:{pow},
体质:{con}, 外貌:{app}, 教育:{edu},
体型:{siz}, 智力:{int}, 总计: {total}\
'''
COC6_CARD_DETAIL_TAMPLATE = '''\
力量:3D6={str_step}={str}
体质:3D6={con_step}={con}
体型:2D6+6={siz_step}={siz}
敏捷:3D6={dex_step}={dex}
外貌:3D6={app_step}={app}
智力:2D6+6={int_step}={int}
意志:3D6={pow_step}={pow}
教育:3D6+3={edu_step}={edu}
总计: {total}
生命值:{hp}, 魔法值:{mp}, 理智值:{san},
幸运:{luck}, 知识检定:{know}, 灵感:{idea},
资产骰:{money}, 伤害价值:{DB}, 体格:{Build}\
'''

def coc7CreateShort():
    card = {}
    tmp = 0
    for i,v in coc7_constant.BuildCOC7.items():
        card[i] = cal_btree.calculate(v,False)
        tmp += card[i]
    card['total_with_luck'] = tmp
    card['total_without_luck'] = tmp - card['luck']
    return card

def coc7CreateDetail():
    card = {}
    tmp = 0
    for i,v in coc7_constant.BuildCOC7.items():
        _,val,step = cal_btree.calculate(v)
        card[i] = val
        card[i+'_step'] = step
        tmp += val
    card['total_with_luck'] = tmp
    card['total_without_luck'] = tmp - card['luck']
    for i,v in coc7_constant.AutoCalCOC7.items():
        exp = v.format_map(card)
        _,val,step = cal_btree.calculate(exp)
        card[i] = int(val)
        card[i+'_step'] = step
    card.update(coc7BuildDB(card['str']+card['siz']))
    return card

def coc6BuildDB(both):
    card = {}
    card['DB'] = None
    for i,v,j in coc7_constant.COC6_DB_BUILD:
        if both <= j :
            card['DB'] = v
            card['Build'] = i
            break
    if card['DB'] == None:
        build = (both-25)//16+1
        card['DB'] = '+{0}d6'.format(build)
        card['Build'] = build
    return card

# coc6
def coc6CreateShort():
    card = {}
    tmp = 0
    for i,v in coc7_constant.BuildCOC6.items():
        card[i] = cal_btree.calculate(v,False)
        tmp += card[i]
    card['total'] = tmp
    return card

def coc6CreateDetail():
    card = {}
    tmp = 0
    for i,v in coc7_constant.BuildCOC6.items():
        _,val,step = cal_btree.calculate(v)
        card[i] = val
        card[i+'_step'] = step
        tmp += val
    card['total'] = tmp
    for i,v in coc7_constant.AutoCalCOC6.items():
        exp = v.format_map(card)
        _,val,step = cal_btree.calculate(exp)
        card[i] = int(val)
        card[i+'_step'] = step
    card.update(coc6BuildDB(card['str']+card['siz']))
    return card

def coc7BuildDB(both):
    card = {}
    card['DB'] = None
    for i,v,j in coc7_constant.COC7_DB_BUILD:
        if both <= j :
            card['DB'] = v
            card['Build'] = i
            break
    if card['DB'] == None:
        build = (both-125)//80+1
        card['DB'] = '+{0}d6'.format(build)
        card['Build'] = build
    return card

def callCOC(msg_obj,RainyDice,message:str,User_ID,Group_Platform,Group_ID):
    card_version = 7
    flag_detail = False
    cnt = 1
    # 7d 7
    restr = 'coc([67])?(d)?\s*(\d*)'
    reobj = re.match(restr,message)
    if not reobj:
        return message_send.Msg_Reply(RainyDice.GlobalVal.GlobalMsg['InputErr'])
    res = reobj.groups()
    if res[0] != None:
        card_version = int(res[0])
    if res[1] != None:
        flag_detail = True
    if res[2] != None and res[2] != '':
        cnt = int(res[2])
    reply_obj = message_send.Msg_Reply(RainyDice.GlobalVal.GlobalMsg['NewRandCard'],{'card_type' : 'COC{0}版'.format(card_version)})
    cardlst = []
    if flag_detail:
        if card_version == 7:
            reply = COC7_CARD_DETAIL_TAMPLATE.format_map(coc7CreateDetail())
        else:
            reply = COC6_CARD_DETAIL_TAMPLATE.format_map(coc6CreateDetail())
    else:
        if card_version == 7:
            tmplst=[]
            tmpcnt = 0
            for i in range(cnt):
                tmplst.append(COC7_CARD_SHORT_TAMPLATE.format_map(coc7CreateShort()))
                tmpcnt += 1
                if tmpcnt == 5:
                    cardlst.append('\n\n'.join(tmplst))
                    tmplst = []
                    tmpcnt = 0
        else:
            tmplst=[]
            tmpcnt = 0
            for i in range(cnt):
                tmplst.append(COC6_CARD_SHORT_TAMPLATE.format_map(coc6CreateShort()))
                tmpcnt += 1
                if tmpcnt == 5:
                    cardlst.append('\n\n'.join(tmplst))
                    tmplst = []
                    tmpcnt = 0
        if tmplst != []:
            cardlst.append('\n\n'.join(tmplst))
        reply = '\f'.join(cardlst)
    reply_obj.extend('',{'card':reply})
    return reply_obj
