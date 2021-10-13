# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  /
    /_/|_/_/ |_/___/_/|_/   /_/

    RainyDice 跑团投掷机器人服务 by RainyZhou
        JRRP 模块

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

import hashlib
import time

def getJrrpInt(hash,min:int=1,max:int=100,step:int=1):
    '通过小数值返回一个区间内的整数，区间为 [min,max]'
    if min > max or step <= 0:
        raise ValueError(min,max,step)
    return int((max-min+1)/step*hash)*step+min

def getJrrpRandom(userid,platform,*salt):
    '获取md5值用于生成jrrp，返回[0,1)的小数'
    # 把每段之前都加上标识符，防止互相干扰
    date = time.strftime('&date-%Y-%m-%d',time.localtime())
    uid = '&userid-'+str(userid)
    platform_str = '&platform-'+str(platform)
    salt_str = '&salt-'+str(salt)
    hashtmp = hashlib.new('md5')
    hashtmp.update(date.encode('utf-8'))
    hashtmp.update(uid.encode('utf-8'))
    hashtmp.update(platform_str.encode('utf-8'))
    hashtmp.update(salt_str.encode('utf-8'))
    # print(txt,int(txt,16))
    return int(hashtmp.hexdigest(),16)/(1<<128)

def callJrrp(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID):
    rand = getJrrpRandom(User_ID,plugin_event.platform['platform'],plugin_event.base_info['self_id'])
    jrrpint = getJrrpInt(rand)
    user_name = RainyDice.user[Group_Platform][User_ID]['U_Name']
    # 'strJrrpReply' : '{username}的今日人品值: {jrrp}'
    reply =  RainyDice.GlobalVal.GlobalMsg['strJrrpReply']
    fmtdict = {
        'username' : user_name,
        'jrrp' : jrrpint
    }
    reply = reply.format_map(fmtdict)
    return 0,False,reply
