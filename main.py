# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  /
    /_/|_/_/ |_/___/_/|_/   /_/

    RainyDice 跑团投掷机器人服务 by RainyZhou
        主文件
    其中编写内容有参考 仑质编写的[OlivaDice]<http://oliva.dice.center/> 特此鸣谢！

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
import os
import time
import sys
import importlib
import OlivOS
from rainydice import RainyDice_UpdateExplain as explain
from rainydice.dice import rolldice
from rainydice.diceClass import Dice
from rainydice.cocRankCheckDefault import create_cocRankCheck
from rainydice import dice_command
import json
# global RainyDice
class Event(object):
    # 初始化
    def init(plugin_event, Proc):       # plugin_models_tmp.main.Event.init(plugin_event = None, Proc = self)
        if sys.version_info.major != 3 or sys.version_info.minor != 7:
            Proc.log(3,'警告：RainyDice在 python 3.7.x 中编写，当前 python 版本：'+sys.version_info.major.__str__()+'.'+sys.version_info.minor.__str__()+'.'+sys.version_info.micro.__str__()+' 不保证功能全部适配')
        bot_init(plugin_event, Proc)
        logtxt = 'RainyDice机器人['+RainyDice.bot.data['name'] + ']已加载完毕，['
        for i,v in RainyDice.platform_dict.items():
            logtxt = logtxt+ i+']共加载群组'+str(len(RainyDice.group[v]['group_list']))+'个，用户'+str(len(RainyDice.user[v]['user_list']))+'个；['
        logtxt = logtxt[:-2]
        Proc.log(2,logtxt)

    def private_message(plugin_event, Proc):
        private_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        group_reply(plugin_event, Proc)

#    def poke(plugin_event, Proc):
#        poke_reply(plugin_event, Proc)
#        pass
    def save(plugin_event, Proc):
        Proc.log(2,'Rainy Dice Save')
        pass
    # onebot框架heartbeat
    def heartbeat(plugin_event, Proc):
        # 每次heartbeat检测当前cpu使用情况
        if dice_command.check_system_status.CpuPercent().percent >=90:
            Proc.log(3,'cpu 当前使用百分比超90%！')
        # heartbeat_reply(plugin_event,Proc)
    def group_file_upload(plugin_event, Proc):
        pass
    def group_message_recall(plugin_event, Proc):
        group_message_recall_reply(plugin_event, Proc)

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
    if not os.path.exists(Data_Path+'/log'):
        os.mkdir(Data_Path+'/log')
    if not os.path.exists(Data_Path+'/temp'):
        os.mkdir(Data_Path+'/temp')
    if not os.path.exists(Data_Path+'/PublicDeck'):
        os.mkdir(Data_Path+'/PublicDeck')

    try:
        with open(Data_Path+'/conf/ignore.json', 'r', encoding = 'utf-8') as ignore_conf_f:
            ignore_conf = json.loads(ignore_conf_f.read())
            proc.log(0,'已读取RainyDice配置文件 ignore.json')
    except:
        proc.log(2,'未找到RainyDice配置文件 ignore.json ，即将新建...')
        ignore_conf = create_ignore_conf(Data_Path=Data_Path,Proc=proc)
    if ignore_conf == None:
        proc.log(3,'RainyDice配置文件 ignore.json 错误，即将新建...')
        ignore_conf = create_ignore_conf(Data_Path=Data_Path,Proc=proc)
    if os.path.isfile(Data_Path+'/conf/rankcheck.py'):
        try:
            rankcheck = importlib.import_module('plugin.data.rainydice.conf.rankcheck')
            cocRankCheck = rankcheck.cocRankCheck
        except:
            cocRankCheck=create_cocRankCheck(Data_Path+'/conf/rankcheck.py')
            proc.log(3,'RainyDice配置文件 rankcheck.py 错误，即将新建...')
    else:
        cocRankCheck=create_cocRankCheck(Data_Path+'/conf/rankcheck.py')
        proc.log(2,'RainyDice配置文件 rankcheck.py 不存在，即将新建...')
    dice_command.check_system_status.CpuPercent()
    global RainyDice
    RainyDice = Dice(Data_Path,log=proc.log,ignore=ignore_conf,cocRankCheck=cocRankCheck)

# 创建ignore文件
def create_ignore_conf(Data_Path= '',Proc=None):
    f_ignore_conf = open(Data_Path+'/conf/ignore.json',"w",encoding="utf-8")
    default_ignore_conf = '''{
    "ignore" : true,
    "qq":{
        "group":[-1],
        "user":[-1]
    },
    "telegram":{
        "group":[-1],
        "user":[-1]
    },
    "dodo":{
        "group":[-1],
        "user":[-1]
    }
}'''

    f_ignore_conf.write(default_ignore_conf)
    f_ignore_conf.close()
    conf = {
        "ignore" : True,
        "qq":{
            "group":[-1],
            "user":[-1]
        },
        "telegram":{
            "group":[-1],
            "user":[-1]
        },
        "dodo":{
            "group":[-1],
            "user":[-1]
        }
    }
    return conf
def private_reply(plugin_event, Proc):
    # print(plugin_event.data)
    # {'font': 0, 'message': '。r', 'message_id': -2028246266, 'message_type': 'private', 'post_type': 'message', 'raw_message': '。r', 'self_id': 123456, 'sender': {'age': 0, 'nickname': 'xxx', 'sex': 'unknown', 'user_id': 654321}, 'sub_type': 'friend', 'target_id': 123456, 'time': 1632070731, 'user_id': 654321}
    User_ID = int(plugin_event.data.user_id)
    message = plugin_event.data.message
    Platform = RainyDice.platform_dict[plugin_event.platform['platform']]
    if User_ID not in RainyDice.user[Platform]['user_list']:  # 创建新用户
        RainyDice.user.add_user(U_Platform=Platform,U_ID=User_ID,sender = plugin_event.data.sender)
    if message == '.bot' or message == '。bot' or message == '/bot':    # 私聊回应 .bot
        plugin_event.send('private',User_ID,RainyDice.GlobalVal.GlobalMsg['BotMsg'].format(version=RainyDice.basic.version.fullversion))
        return None
    if message[0] not in RainyDice.GlobalVal.Command_Start_Sign :
        return None
    message=message[1:].lower()
    command_run(message,plugin_event,Proc,User_ID,Platform,0)
def heartbeat_reply(plugin_event,proc):
    pass

def group_reply(plugin_event, Proc):
    Group_Platform = RainyDice.platform_dict[plugin_event.platform['platform']]
    Group_ID = int(plugin_event.data.group_id)
    User_ID = int(plugin_event.data.user_id)
    message = plugin_event.data.message.lstrip()
    # 如果群组位于ignore list中则直接无视，不进行任何操作
    if Group_ID in RainyDice.ignore[plugin_event.platform['platform']]['group'] and RainyDice.ignore['ignore']==True:           # 黑名单模式（仅列表中不回应）
        return None
    elif Group_ID not in RainyDice.ignore[plugin_event.platform['platform']]['group'] and RainyDice.ignore['ignore']==False:    # 白名单模式（仅列表中回应）
        return None
    # 是否在指令开头at bot
    at_bot = '[CQ:at,qq=' + str(plugin_event.base_info['self_id']) + ']'
    isAtBot = str.find(message,at_bot,0,len(at_bot))==0
    if isAtBot:
        message = message[len(at_bot):]
    message = str.lstrip(message)
    if Group_ID not in RainyDice.group[Group_Platform]['group_list']:
        RainyDice.group.add_group(Group_Platform=Group_Platform,Group_ID=Group_ID)
    if User_ID not in RainyDice.user[Group_Platform]['user_list']:  # 创建新用户
        RainyDice.user.add_user(U_Platform=Group_Platform,U_ID=User_ID,sender = plugin_event.data.sender)
    # 记录log模块
    isLogOn = False
    if RainyDice.group[Group_Platform][Group_ID]['isLogOn']:
        isLogOn= True
        # 【log记录】
        if 0 in dict.keys(RainyDice.group[Group_Platform][Group_ID]['log']):
            log_name = RainyDice.group[Group_Platform][Group_ID]['log'][0]
        else:
            log_name = 'log_{0:d}_{1:d}_{2:d}'.format(Group_Platform,Group_ID,time.time().__int__())
            RainyDice.group.set('log',(0,log_name),Group_Platform,Group_ID)
            dice_command.chat_log.log_create(RainyDice.bot,log_name)
        log_name = RainyDice.group[Group_Platform][Group_ID]['log'][0]
        if User_ID in RainyDice.group[Group_Platform][Group_ID]['name']:
            user_name = RainyDice.group[Group_Platform][Group_ID]['name'][User_ID]
        else:
            user_name = RainyDice.user[Group_Platform][User_ID]['U_Name']
        log_time = plugin_event.base_info['time']
        group_name = RainyDice.group[Group_Platform][Group_ID]['Group_Name']
        dice_command.chat_log.log_msg(RainyDice.bot,log_name=log_name,platform=Group_Platform,user_id=User_ID,user_name=user_name,user_text=plugin_event.data.message,log_time=log_time,group_id=Group_ID,group_name=group_name)
    if message == '.bot' or message == '。bot' or message == '/bot':    # 私聊回应 .bot
        plugin_event.send('private',User_ID,RainyDice.GlobalVal.GlobalMsg['BotMsg'].format(version=RainyDice.basic.version.fullversion))
        return None
    elif message == '.bot on' or message == '。bot on' or message == '/bot on':    # .bot on 开启骰娘
        RainyDice.group.set('isBotOn',1,Group_Platform,Group_ID)
        reply = RainyDice.GlobalVal.GlobalMsg['BotOnReply'].format(bot_name=RainyDice.bot.data['name'])
        plugin_event.reply(reply)
        return None
    elif message == '.bot off' or message == '。bot off' or message == '/bot off':    # .bot off 关闭骰娘
        RainyDice.group.set('isBotOn',0,Group_Platform,Group_ID)
        reply = RainyDice.GlobalVal.GlobalMsg['BotOffReply'].format(bot_name=RainyDice.bot.data['name'])
        plugin_event.reply(reply)
        return None
    # 如果群聊关闭且未at bot，则不回应
    if RainyDice.group[Group_Platform][Group_ID]['isBotOn'] == 0 and isAtBot == False:    # 如果没开启且没at bot 则不处理消息
        return None
    if message =='' or message[0] not in RainyDice.GlobalVal.Command_Start_Sign :
        return None
    message=message[1:].lower()
    command_run(message,plugin_event,Proc,User_ID,Group_Platform,Group_ID,isLogOn)
    return None

def group_message_recall_reply(plugin_event, Proc):
    Group_Platform = RainyDice.platform_dict[plugin_event.platform['platform']]
    Group_ID = int(plugin_event.data.group_id)
    User_ID = int(plugin_event.data.user_id)
    Operator_ID = int(plugin_event.data.operator_id)
    message_id = int(plugin_event.data.message_id)
    # 如果群组位于ignore list中则直接无视，不进行任何操作
    if Group_ID in RainyDice.ignore[plugin_event.platform['platform']]['group'] and RainyDice.ignore['ignore']==True:           # 黑名单模式（仅列表中不回应）
        return None
    elif Group_ID not in RainyDice.ignore[plugin_event.platform['platform']]['group'] and RainyDice.ignore['ignore']==False:    # 白名单模式（仅列表中回应）
        return None
    elif not RainyDice.group[Group_Platform][Group_ID]['isBanRecall'] or User_ID != Operator_ID:
        return None
    #[CQ:reply,text=Hello World,qq=10086,time=3376656000,seq=5123]
    reply = '[CQ:reply,id={id}]#'.format(id=message_id)
    plugin_event.reply(reply)

def command_run(message:str,plugin_event,Proc,User_ID:int,Platform:int,Group_ID=0,isLogOn=False):
    msg_send = dice_command.message_send.Message_Send_All(RainyDice=RainyDice,plugin_event=plugin_event,proc=Proc,flag_proc_log=True,flag_chat_log=isLogOn)
    # cal = rainydice.rainydice.calculate.RPN()
    Group_Platform = Platform
    rd = rolldice(RainyDice.cocRankCheck)
    message = message.strip()
    def func_reply(reply:str,isLogOn=False,fmtdict={}):
        '直接回复消息，同时记录log'
        replyobj = dice_command.message_send.Msg_Reply(reply,formatDict=fmtdict,flag_chat_log=isLogOn)
        msg_send.attach(replyobj)
        msg_send.send()
    if message.startswith('ra') or message.startswith('rc'):
        if message == 'ra' or message == 'rc':
            func_reply(isLogOn=isLogOn,reply=RainyDice.GlobalVal.getHelpDoc('ra'))
        else:
            message=message[2:]
            # 返回 (状态码(判断是否正常，或错误类型，目前没搞只是留好接口),是否为多处回复（T/F）,单回复信息或(('reply',message),('send',target_type,target_id,message),...))
            reply = dice_command.ra_command.callRA(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
            msg_send.attach(reply)
            msg_send.send()
        return 1
    elif message.startswith('sc'):
        if message == 'sc':
            func_reply(isLogOn=isLogOn,reply=RainyDice.GlobalVal.getHelpDoc('sc'))
        else:
            message=message[2:].strip()
            # 返回 (状态码,是否为多处回复（T/F）,单回复信息或(('reply',message),('send',target_type,target_id,message),...))
            status,isMultiReply ,reply = rd.SC(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
            dice_command.chat_log.send_reply(RainyDice=RainyDice,plugin_event=plugin_event,proc=Proc,status=status,isMultiReply=isMultiReply,reply=reply,Group_Platform=Group_Platform,Group_ID=Group_ID,isLogOn=isLogOn)
        return 1
    elif message.startswith('st'):
        if message == 'st':
            func_reply(isLogOn=isLogOn,reply=RainyDice.GlobalVal.getHelpDoc('st'))
        else:
            message=str.strip(message[2:])
            status,isMultiReply ,reply = rd.ST(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
            dice_command.chat_log.send_reply(RainyDice=RainyDice,plugin_event=plugin_event,proc=Proc,status=status,isMultiReply=isMultiReply,reply=reply,Group_Platform=Group_Platform,Group_ID=Group_ID,isLogOn=isLogOn)
        return 1
    elif message.startswith('recall'):
        if Group_ID == 0 or message == 'recall':
            func_reply(isLogOn=isLogOn,reply=RainyDice.GlobalVal.getHelpDoc('recall'))
        else:
            message = str.strip(message[6:])
            status,isMultiReply ,reply = rd.RECALL(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
            dice_command.chat_log.send_reply(RainyDice=RainyDice,plugin_event=plugin_event,proc=Proc,status=status,isMultiReply=isMultiReply,reply=reply,Group_Platform=Group_Platform,Group_ID=Group_ID,isLogOn=isLogOn)
        return 1
    elif message.startswith('r'):
        if len(message) == 1:
            message = 'r1d100'
        message=message[1:]
        status,isMultiReply ,reply = rd.RD(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
        dice_command.chat_log.send_reply(RainyDice=RainyDice,plugin_event=plugin_event,proc=Proc,status=status,isMultiReply=isMultiReply,reply=reply,Group_Platform=Group_Platform,Group_ID=Group_ID,isLogOn=isLogOn)
        return 1
    elif message.startswith('nn'):
        if message == 'nn':
            func_reply(isLogOn=isLogOn,reply=RainyDice.GlobalVal.getHelpDoc('nn'))
        else:
            message=str.strip(message[2:])
            name = str.strip(message)
            RainyDice.user.set('U_Name',name,Group_Platform,User_ID)
            reply = RainyDice.GlobalVal.GlobalMsg['nnReply'].format(User_Name=plugin_event.data.sender['nickname'],New_Name=name)
            func_reply(isLogOn=isLogOn,reply=reply)
        return 1
    elif message.startswith('li'):
        status,isMultiReply ,reply = rd.LI(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
        dice_command.chat_log.send_reply(RainyDice=RainyDice,plugin_event=plugin_event,proc=Proc,status=status,isMultiReply=isMultiReply,reply=reply,Group_Platform=Group_Platform,Group_ID=Group_ID,isLogOn=isLogOn)
        return 1
    elif message.startswith('ti'):
        status,isMultiReply ,reply = rd.TI(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
        dice_command.chat_log.send_reply(RainyDice=RainyDice,plugin_event=plugin_event,proc=Proc,status=status,isMultiReply=isMultiReply,reply=reply,Group_Platform=Group_Platform,Group_ID=Group_ID,isLogOn=isLogOn)
        return 1
    elif message.startswith('setcoc'):
        if message == 'setcoc':
            func_reply(isLogOn=isLogOn,reply=RainyDice.GlobalVal.getHelpDoc('setcoc'))
        else:
            message=str.strip(message[6:])
            status,isMultiReply ,reply = rd.SETCOC(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
            dice_command.chat_log.send_reply(RainyDice=RainyDice,plugin_event=plugin_event,proc=Proc,status=status,isMultiReply=isMultiReply,reply=reply,Group_Platform=Group_Platform,Group_ID=Group_ID,isLogOn=isLogOn)
        return 1
    elif message.startswith('en'):
        if message == 'en':
            func_reply(isLogOn=isLogOn,reply=RainyDice.GlobalVal.getHelpDoc('en'))
        else:
            message=str.strip(message[2:])
            status,isMultiReply ,reply = rd.EN(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
            dice_command.chat_log.send_reply(RainyDice=RainyDice,plugin_event=plugin_event,proc=Proc,status=status,isMultiReply=isMultiReply,reply=reply,Group_Platform=Group_Platform,Group_ID=Group_ID,isLogOn=isLogOn)
        return 1
    elif message.startswith('coc'):
        if message == 'coc':
            message = 'coc 1'
        reply_obj=dice_command.coc_card_new.callCOC(msg_send,RainyDice,message,User_ID,Group_Platform,Group_ID)
        msg_send.attach(reply_obj)
        msg_send.send()
        return 1
    elif message.startswith('master'):
        if message == 'master':
            if User_ID == RainyDice.bot.data[plugin_event.platform['platform']+'_master']:
                reply = '您已是{botname}的master！'.format(botname=RainyDice.bot.data['name'])
                func_reply(isLogOn=isLogOn,reply=reply)
                # master本人发送.master
            elif RainyDice.bot.data[plugin_event.platform['platform']+'_master'] == 0:
                RainyDice.bot.data[plugin_event.platform['platform']+'_master'] = User_ID
                RainyDice.bot.set()
                reply = '已将您设置成为{botname}的master'.format(botname=RainyDice.bot.data['name'])
                func_reply(isLogOn=isLogOn,reply=reply)
            else:
                reply = RainyDice.GlobalVal.getGlobalMsg('authorationFailed')
                func_reply(isLogOn=isLogOn,reply=reply)
        else:
            pass
        return 1
    elif message.startswith('admin'):
        if message == 'admin':
            if User_ID in RainyDice.bot.data[plugin_event.platform['platform']+'_admin'] == 0:
                reply = '您已是{botname}的admin！'.format(botname=RainyDice.bot.data['name'])
                func_reply(isLogOn=isLogOn,reply=reply)
            else:
                reply = RainyDice.GlobalVal.getGlobalMsg('authorationFailed')
                func_reply(isLogOn=isLogOn,reply=reply)
        else:
            pass
        return 1
    elif message.startswith('log'):
        if Group_ID == 0 or message == 'log':
            func_reply(isLogOn=isLogOn,reply=RainyDice.GlobalVal.getHelpDoc('log'))
        else:
            message = str.strip(message[3:])
            # 直接内部发送
            dice_command.message_send.log_cmd(msg_send,RainyDice,message,User_ID,Group_Platform,Group_ID)
        return 1
    elif message.startswith('help'):
        if message == 'help':
            func_reply(isLogOn=isLogOn,reply=RainyDice.GlobalVal.getHelpDoc('help'))
        else:
            message = message[4:].strip()
            func_reply(isLogOn=isLogOn,reply=RainyDice.GlobalVal.getHelpDoc(message))
        return 1
    elif message.startswith('version'):
        reply = 'RainyDice Version: \n'+RainyDice.basic.version.fullversion+'\n'+explain
        func_reply(isLogOn=isLogOn,reply=reply)
        return 1
    elif message.startswith('system'):
        if message == 'system':
            func_reply(isLogOn=isLogOn,reply=RainyDice.GlobalVal.getHelpDoc('system'))
        elif message[6:].strip().startswith('status') or message[6:].strip().startswith('stats'):
            reply = dice_command.system_command.getSysState(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
            func_reply(isLogOn=isLogOn,reply=reply)
        elif message[6:].strip().startswith('restart'):
            dice_command.system_command.callSysRestart(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID,msg_send)
        else:
            reply = '未知指令 '+message[6:]
            func_reply(isLogOn=isLogOn,reply=reply)
        return 1
    elif message.startswith('jrrp'):
        status,isMultiReply ,reply = dice_command.jrrp_command.callJrrp(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
        dice_command.chat_log.send_reply(RainyDice=RainyDice,plugin_event=plugin_event,proc=Proc,status=status,isMultiReply=isMultiReply,reply=reply,Group_Platform=Group_Platform,Group_ID=Group_ID,isLogOn=isLogOn)
        return 1
    elif message.startswith('draw'):
        if message == 'draw':
            func_reply(isLogOn=isLogOn,reply=RainyDice.GlobalVal.getHelpDoc('draw'))
        else:
            message = message[4:].strip()
            status,isMultiReply ,reply = dice_command.draw_command.callDraw(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
            dice_command.chat_log.send_reply(RainyDice=RainyDice,plugin_event=plugin_event,proc=Proc,status=status,isMultiReply=isMultiReply,reply=reply,Group_Platform=Group_Platform,Group_ID=Group_ID,isLogOn=isLogOn)
        return 1
    elif message.startswith('dismiss'):
        if message == 'dismiss':
            func_reply(isLogOn=isLogOn,reply=RainyDice.GlobalVal.getHelpDoc('draw'))
        else:
            message = message[4:].strip()
            status,isMultiReply ,reply = dice_command.draw_command.callDraw(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
            dice_command.chat_log.send_reply(RainyDice=RainyDice,plugin_event=plugin_event,proc=Proc,status=status,isMultiReply=isMultiReply,reply=reply,Group_Platform=Group_Platform,Group_ID=Group_ID,isLogOn=isLogOn)
        return 1
    else:
        return None
