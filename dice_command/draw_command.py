# -*- coding: utf-8 -*-
'''
   ___  ___   _____  ____  __
  / _ \/ _ | /  _/ |/ /\ \/ /
 / , _/ __ |_/ //    /  \  / 
/_/|_/_/ |_/___/_/|_/   /_/  
                             
    draw 抽卡模块
    内置牌堆详见 card_deck.py

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

from random import randint
from rainydice.dice_command import card_deck
from rainydice.dice_command import cal_btree
# import card_deck
# import cal_btree

def strPublicDeckKey():
    '返回所有公共牌堆的名称'
    keylist = []
    for thiskey in card_deck.mPublicDeck.keys():
        if thiskey[0] != '_':
            # 判断私有牌堆，即 _ 开头的不输出
            keylist.append(thiskey)
    strkeylist = ','.join(keylist)
    return strkeylist

def drawCard(deckName:str,tempdeck=False,decks:dict={}):
    '抽卡模块，若牌堆不存在则返回 None'
    # print(deckName,tempdeck,decks)
    if deckName not in card_deck.mPublicDeck.keys():
        raise UserWarning(deckName+' not in decks')
    thisdeck = card_deck.mPublicDeck.get(deckName).copy()
    if not tempdeck:
        # 已抽取的卡(避免重复抽取)
        if deckName in decks.keys():
            for cardused in decks[deckName]:
            # 删除此牌堆已经抽取的内容, cardused 为已经抽取的卡
                thisdeck.remove(cardused)
        else:
            decks[deckName] = []
        # 抽卡
        card = thisdeck[randint(0,len(thisdeck)-1)]
        decks[deckName].append(card)
    else:
        card = thisdeck[randint(0,len(thisdeck)-1)]
    lq = str.find(card,'{')
    rq = str.find(card,'}',lq+1)
    while lq != -1 and rq != -1 and rq-lq > 1: # 当抽到的卡组含有 {xx}时进行进一步抽卡
        tempdeck = False
        draw = card[lq+1:rq]
        if draw[0] == '%':
            tempdeck = True
            draw = draw[1:]
        localdraw,decks = drawCard(deckName=draw,tempdeck=tempdeck,decks=decks)
        card = card.replace(card[lq:rq+1],localdraw,1)
        lq = str.find(card,'{',lq)
        rq = str.find(card,'}',lq+1)
    lq = str.find(card,'[')
    rq = str.find(card,']',lq+1)
    while lq != -1 and rq != -1 and rq-lq > 1: # 当抽到的卡组含有 [xx]时进行进一步运算
        exp = card[lq+1:rq]
        result = cal_btree.calculate(exp,False)
        if result == None:
            result = 0
        card = card.replace(card[lq:rq+1],str(result),1)
        lq = str.find(card,'[',lq)
        rq = str.find(card,']',lq+1)
    # print(card)
    return card,decks

def callDraw(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID):
    user_name = RainyDice.user[Group_Platform][User_ID]['U_Name']
    # 'strDrawReply' : '{username}的进行抽卡: \n{card}'
    reply =  RainyDice.GlobalVal.GlobalMsg['strDrawReply']
    if message == 'help':
        reply = '全牌堆列表：\n'+strPublicDeckKey()
    else:
        try:
            reply = drawCard(message)[0]
        except UserWarning as err:
            reply = '抽卡错误！ '+err.__str__()
    return 0,False,reply

# if __name__ == '__main__':
#     #print(mPublicDeck['凯尔特十字牌阵'][0])
#     #print(strPublicDeckKey())
#     print(drawCard('即时症状')[0])
