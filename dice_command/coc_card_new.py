# -*- coding: utf-8 -*-
'''
   ___  ___   _____  ____  __
  / _ \/ _ | /  _/ |/ /\ \/ /
 / , _/ __ |_/ //    /  \  / 
/_/|_/_/ |_/___/_/|_/   /_/  
                             
    外置牌堆读取至临时数据库

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
from rainydice.dice_command import coc7_constant
# import cal_btree
# import coc7_constant


COC_CARD_SHORT_TAMPLATE = '''\
力量:{力量}, 敏捷:{敏捷}, 意志:{意志}, 
体质:{体质}, 外貌:{外貌}, 教育:{教育}, 
体型:{体型}, 智力:{智力}, 幸运:{幸运}, 
生命:{生命}, 魔法:{魔法}, DB: {DB}
总计: {total_without_luck} / {total_with_luck}
'''

COC_DB_BUILD = [
    (-2,'-2',64),
    (-1,'-1',84),
    (0,'+0',124),
    (1,'+1d4',164),
    (2,'+1d6',204),
    (3,'+2d6',284)
]

COC_CARD_ATTR_TAMPLATE = coc7_constant.BuildCOC7

def creatCardCoc():
    card = {}
    for i,v in COC_CARD_ATTR_TAMPLATE.items():
        v = v.format_map(card)
        card[i] = int(cal_btree.calculate(v,False))
    card = cocAutoCal(card)    
    return card

def cocAutoCal(card):
    STR = card['力量']
    SIZ = card['体型']
    both = STR+SIZ
    card['DB'] = None
    for i,v,j in COC_DB_BUILD:
        if both <= j :
            card['DB'] = v
            card['Build'] = i
            break
    if card['DB'] == None:
        build = (both-125)//80+1
        card['DB'] = '+{0}d6'.format(build)
        card['Build'] = build
    tmp = 0
    for i in ('力量','体质','体型','意志','外貌','智力','敏捷','教育'):
        tmp = tmp + card[i]
    card['total_without_luck'] = tmp
    card['total_with_luck'] = tmp + card['幸运']
    return card

def callCOC(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID):
    ''
    reply = COC_CARD_SHORT_TAMPLATE.format_map(creatCardCoc())
    return 0,False,reply

# if __name__ == '__main__':
#     print(creatCardCoc())
#     print(callCOC(0,0,0,0,0,0,0))