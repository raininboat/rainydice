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
# from rainydice.dice_command import card_deck
from rainydice.dice_command import cal_btree
from rainydice.dice_command import public_deck
# import card_deck
# import cal_btree

def strPublicDeckKey(publicDeck):
    '返回所有公共牌堆的名称'
    keylist = []
    keylistlong = []
    cnt = 0
    for thiskey in publicDeck.decks.keys():  # card_deck.mPublicDeck.keys()
        cnt = cnt + 1
        if thiskey[0] != '_':
            # 判断私有牌堆，即 _ 开头的不输出
            keylist.append(thiskey)
        if cnt == 40:
            # 每页显示50个牌堆
            keylistlong.append(','.join(keylist))
            keylist = []
            cnt = 0
    keylistlong.append(','.join(keylist))
    strkeylist = '\f'.join(keylistlong)
    return strkeylist

def drawCard(deckName:str,deckall,tempdeck=False,decks:dict={}):
    '抽卡模块，若牌堆不存在则返回 None'
    # print(deckName,tempdeck,decks)
    thisdeck = getThisDeck(deckName,deckall,decks)
    if thisdeck == None:
        return '{'+deckName+'}',decks
    elif len(thisdeck) == 0:
        # 对空卡堆进行排除
        raise UserWarning('卡组无内容 - '+ deckName + '\n已抽取卡片 - '+decks.__str__())
    card = thisdeck[randint(0,len(thisdeck)-1)]
    if not tempdeck:
        if deckName not in decks.keys():
            decks[deckName] = {}
        if card  in decks[deckName].keys():
            decks[deckName][card] = decks[deckName][card] + 1
        else:
            decks[deckName][card] = 1
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
    if card.startswith('::'):
        s = card.find('::',2)
        card = card[s+2:]
    # print(card)
    return card,decks

def getThisDeck(deckName,deckall,decks:dict={}):
    if deckName not in deckall.keys():
        return None
        raise UserWarning(deckName+' not in decks')
    tmpdeck = []
    if deckName in decks.keys():
        usedCard = decks[deckName]
    else:
        usedCard = {}
    # print('已抽取卡片',usedCard)
    for deckkeyRaw in deckall.get(deckName):
        cnt = 1
        if deckkeyRaw.startswith('::'):
            s = deckkeyRaw.find('::',2)
            if s != -1:
                cnt = int(deckkeyRaw[2:s])
        if deckkeyRaw in usedCard.keys():
            cnt = cnt - usedCard[deckkeyRaw]
        if cnt > 0:
            tmpdeck.extend([deckkeyRaw]*cnt)
    return tmpdeck

def callDraw(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID):
    user_name = RainyDice.user[Group_Platform][User_ID]['U_Name']
    # 'strDrawReply' : '{username}的进行抽卡: \n{card}'
    reply =  RainyDice.GlobalVal.GlobalMsg['strDrawReply']
    if message == 'help':
        reply = '全牌堆列表：\n'+strPublicDeckKey(RainyDice.publicDeck)
    else:
        try:
            if message in RainyDice.publicDeck.decks.keys():
                deckinfo = RainyDice.publicDeck.metaInfo[RainyDice.publicDeck.decks[message]]
            else:
                raise UserWarning(message + ' not found')
            deckall = public_deck.loadDeck(RainyDice.data_path,deckinfo)
            reply = reply.format(username=user_name,card=drawCard(message,deckall)[0])
        except UserWarning as err:
            reply = '抽卡错误！ '+err.__str__()
    return 0,False,reply

# if __name__ == '__main__':
#     pass
#     #print(mPublicDeck['凯尔特十字牌阵'][0])
#     #print(strPublicDeckKey())
#     #print(drawCard('塔罗牌阵')[0])
