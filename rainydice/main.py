# -*- coding: utf-8 -*-
'''
   ___  ___   _____  ____  __
  / _ \/ _ | /  _/ |/ /\ \/ /
 / , _/ __ |_/ //    /  \  / 
/_/|_/_/ |_/___/_/|_/   /_/  
                             
    测试内容

'''


import re
import OlivOS
import rainydice
import os
import sys
import json
import sqlite3
from rainydice.dice import rolldice
from rainydice.diceClass import Dice
global RainyDice
class Event(object):
    # 初始化
    def init(plugin_event, Proc):       # plugin_models_tmp.main.Event.init(plugin_event = None, Proc = self) 
        bot_init(plugin_event, Proc)
        Proc.log(2,'RainyDice机器人['+RainyDice.bot.data['name'] + ']已加载完毕')

    def private_message(plugin_event, Proc):
        private_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        group_reply(plugin_event, Proc)

    def poke(plugin_event, Proc):
#        poke_reply(plugin_event, Proc)
        pass
    def save(plugin_event, Proc):
        pass
    # onebot框架heartbeat
    def heartbeat(plugin_event, Proc):
        heartbeat_reply(plugin_event,Proc)
        pass
    def group_file_upload(plugin_event, Proc):
        pass


def bot_init(plugin_event,proc):
    OlivOS_Path = sys.path[0]
    # os.environ['path'] += ';'+sys.path[0]+'/plugin/app/rainydice/lib/dll'
    Data_Path = OlivOS_Path + '/plugin/data/rainydice'
    if not os.path.exists(Data_Path):
        proc.log(0,'正在新建文件夹')
        os.mkdir(Data_Path)
    if not os.path.exists(Data_Path+'/conf'):
        os.mkdir(Data_Path+'/conf')
    if not os.path.exists(Data_Path+'/group'):
        os.mkdir(Data_Path+'/group')
    if not os.path.exists(Data_Path+'/user'):
        os.mkdir(Data_Path+'/user')
    global RainyDice
    RainyDice = Dice(Data_Path,proc.log)


def private_reply(plugin_event, Proc):
    pass
def heartbeat_reply(plugin_event,proc):
    pass

def group_reply(plugin_event, Proc):
    message = plugin_event.data.message
    # 是否在指令开头at bot
    at_bot = '[CQ:at,qq=' + str(plugin_event.base_info['self_id']) + ']'
    isAtBot = str.find(message,at_bot,0,len(at_bot))==0
    if isAtBot:
        message = message[len(at_bot):]
    message = str.lstrip(message)
    Group_Platform = RainyDice.platform_dict[plugin_event.platform['platform']]
    Group_ID = int(plugin_event.data.group_id)
    User_ID = int(plugin_event.data.user_id)
    if Group_ID not in RainyDice.group[Group_Platform]['group_list']:
        RainyDice.group.add_group(Group_Platform=Group_Platform,Group_ID=Group_ID)
    # print(RainyDice.group)
    if RainyDice.group[Group_Platform][Group_ID]['Group_isBotOn'] == 0 and isAtBot == False:
        if message == '.bot' or message == '。bot' or message == '/bot':    # 私聊回应 .bot
            plugin_event.send('private',User_ID,RainyDice.GlobalVal.GlobalMsg['BotMsg'])
        return None
    # 记录log模块先不写
    # 【预留位置】
    # 如果群聊关闭且未at bot，则不回应
    if message[0] not in RainyDice.GlobalVal.Command_Start_Sign :
        return None
    if User_ID not in RainyDice.user[Group_Platform]['user_list']:  # 创建新用户
        RainyDice.user.add_user(U_Platform=Group_Platform,U_ID=User_ID)
    message=message[1:].lower()
    message = message.rstrip()
    rd = rolldice()
    # cal = rainydice.rainydice.calculate.RPN()
    if message.startswith('ra') or message.startswith('rc'):
        if message == 'ra' or message == 'rc':
            plugin_event.reply(RainyDice.GlobalVal.getHelpDoc('ra'))
        else:
            message=message[2:].rstrip()
            # 返回 (状态码,是否为多处回复（T/F）,单回复信息或(('reply',message),('send',target_type,target_id,message),...))
            status,isMultiReply ,reply = rd.RA(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
            if isMultiReply:
                for replypack in reply:
                    if replypack[0] == 'reply':
                        plugin_event.reply(replypack[1])
                    elif replypack[0] == 'send':
                        target_type = replypack[1]
                        target_id = replypack[2]
                        reply_msg = replypack[3]
                        plugin_event.send(target_type,target_id,reply_msg)
            else:
                plugin_event.reply(reply)
        return 1
    elif message.startswith('sc'):
        pass
    elif message.startswith('rb'):
        if message == 'rb':
            plugin_event.reply(RainyDice.GlobalVal.getHelpDoc('ra'))
        else:
            message=message[1:]
            status,isMultiReply ,reply = rd.RA(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
            if isMultiReply:
                for replypack in reply:
                    if replypack[0] == 'reply':
                        plugin_event.reply(replypack[1])
                    elif replypack[0] == 'send':
                        target_type = replypack[1]
                        target_id = replypack[2]
                        reply_msg = replypack[3]
                        plugin_event.send(target_type,target_id,reply_msg)
            else:
                plugin_event.reply(reply)
            pass
        return 1
    elif message.startswith('rp'):
        if message == 'rb':
            plugin_event.reply(RainyDice.GlobalVal.getHelpDoc('ra'))
        else:
            message=message[1:]
            status,isMultiReply ,reply = rd.RA(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
            if isMultiReply:
                for replypack in reply:
                    if replypack[0] == 'reply':
                        plugin_event.reply(replypack[1])
                    elif replypack[0] == 'send':
                        target_type = replypack[1]
                        target_id = replypack[2]
                        reply_msg = replypack[3]
                        plugin_event.send(target_type,target_id,reply_msg)
            else:
                plugin_event.reply(reply)
            pass
        return 1
    elif message.startswith('rh'):
        if message == 'rh':
            pass
        pass
        return 1
    elif message.startswith('rd'):
        if message == 'rd':
            message = '1D100'
        else:
            message = '1'+message[1:]
        status,isMultiReply ,reply = rd.RD(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
        if isMultiReply:
            for replypack in reply:
                if replypack[0] == 'reply':
                    plugin_event.reply(replypack[1])
                elif replypack[0] == 'send':
                    target_type = replypack[1]
                    target_id = replypack[2]
                    reply_msg = replypack[3]
                    plugin_event.send(target_type,target_id,reply_msg)
        else:
            plugin_event.reply(reply)
        return 1
    elif message.startswith('st'):
        pass
    elif message.startswith('log'):
        pass
    elif message.startswith('help'):
        pass
    elif message.startswith('r'):
        if len(message) == 1:
            message = 'r1d100'
        message=message[1:]
        status,isMultiReply ,reply = rd.RD(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
        plugin_event.reply(reply)
        return 1
    elif message.startswith('nn'):
        pass
    elif message.startswith('master'):
        pass
    elif message.startswith('admin'):
        pass
    elif message.startswith('bot'):
        pass

    
