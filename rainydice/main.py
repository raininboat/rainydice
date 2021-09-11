# -*- coding: utf-8 -*-
'''
   ___  ___   _____  ____  __
  / _ \/ _ | /  _/ |/ /\ \/ /
 / , _/ __ |_/ //    /  \  / 
/_/|_/_/ |_/___/_/|_/   /_/  
                             
    测试内容

'''

# import OlivOS
# import rainydice
import os
from plugin.app import rainydice
import sys
from rainydice.dice import rolldice
from rainydice.diceClass import Dice
from rainydice.cocRankCheckDefault import create_cocRankCheck
#from .data.rainydice.conf import aaa
import json
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
    try:
        with open(Data_Path+'/conf/ignore.json', 'r', encoding = 'utf-8') as ignore_conf_f:
            ignore_conf = json.loads(ignore_conf_f.read())
            proc.log(0,'已读取RainyDice配置文件 ignore.json') 
    except:
        proc.log(0,'未找到RainyDice配置文件 group.json ，即将新建...')
        ignore_conf = create_ignore_conf(Data_Path=Data_Path,Proc=proc)
    if ignore_conf == None:
        proc.log(0,'RainyDice配置文件 group.json 错误，即将新建...')
        ignore_conf = create_ignore_conf(Data_Path=Data_Path,Proc=proc)
    if os.path.isfile(Data_Path+'/conf/rankcheck.py'):
        try:
            from plugin.data.rainydice.conf.rankcheck import cocRankCheck
        except:
            cocRankCheck=create_cocRankCheck(Data_Path+'/conf/rankcheck.py')
            proc.log(0,'RainyDice配置文件 rankcheck.py 错误，即将新建...')
    else:
        cocRankCheck=create_cocRankCheck(Data_Path+'/conf/rankcheck.py')
        proc.log(0,'RainyDice配置文件 rankcheck.py 不存在，即将新建...')
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
        }
    }
    return conf
def private_reply(plugin_event, Proc):
    print(plugin_event.data)
    pass
def heartbeat_reply(plugin_event,proc):
    pass

def group_reply(plugin_event, Proc):
    Group_Platform = RainyDice.platform_dict[plugin_event.platform['platform']]
    Group_ID = int(plugin_event.data.group_id)
    User_ID = int(plugin_event.data.user_id)
    message = plugin_event.data.message
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
    # print(RainyDice.group)
    if message == '.bot' or message == '。bot' or message == '/bot':    # 私聊回应 .bot
        plugin_event.send('private',User_ID,RainyDice.GlobalVal.GlobalMsg['BotMsg'])
        return None
    elif message == '.bot on' or message == '。bot on' or message == '/bot on':    # .bot on 开启骰娘
        RainyDice.group.set('Group_isBotOn',1,Group_Platform,Group_ID)
        reply = RainyDice.GlobalVal.GlobalMsg['BotOnReply']
        reply = str.replace(reply,'[bot_name]',RainyDice.bot.data['name'])
        plugin_event.reply(reply)
        return None
    elif message == '.bot off' or message == '。bot off' or message == '/bot off':    # .bot off 关闭骰娘
        RainyDice.group.set('Group_isBotOn',0,Group_Platform,Group_ID)
        reply = RainyDice.GlobalVal.GlobalMsg['BotOffReply']
        reply = str.replace(reply,'[bot_name]',RainyDice.bot.data['name'])
        plugin_event.reply(reply)
        return None
    # 记录log模块先不写
    # 【预留位置】
    # 如果群聊关闭且未at bot，则不回应
    if RainyDice.group[Group_Platform][Group_ID]['Group_isBotOn'] == 0 and isAtBot == False:    # 如果没开启且没at bot 则不处理消息
        return None
    if message == '' :
        return None
    if message[0] not in RainyDice.GlobalVal.Command_Start_Sign :
        return None
    if User_ID not in RainyDice.user[Group_Platform]['user_list']:  # 创建新用户
        RainyDice.user.add_user(U_Platform=Group_Platform,U_ID=User_ID,sender = plugin_event.data.sender)
    message=message[1:].lower()
    message = message.rstrip()
    rd = rolldice(RainyDice.cocRankCheck)
    # cal = rainydice.rainydice.calculate.RPN()
    if message.startswith('ra') or message.startswith('rc'):
        if message == 'ra' or message == 'rc':
            plugin_event.reply(RainyDice.GlobalVal.getHelpDoc('ra'))
        else:
            message=message[2:].rstrip()
            # 返回 (状态码(判断是否正常，或错误类型，目前没搞只是留好接口),是否为多处回复（T/F）,单回复信息或(('reply',message),('send',target_type,target_id,message),...))
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
        if message == 'sc':
            plugin_event.reply(RainyDice.GlobalVal.getHelpDoc('sc'))
        else:
            message=message[2:].rstrip()
            # 返回 (状态码,是否为多处回复（T/F）,单回复信息或(('reply',message),('send',target_type,target_id,message),...))
            status,isMultiReply ,reply = rd.SC(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
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
        return 1
    elif message.startswith('rh'):          # 懒得写到dice里面了，直接这样吧(#被拖走)
        if message == 'rh':
            message = '1D100'
        else:
            message = message[2:]
        status,isMultiReply ,reply = rd.RD(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
        reply = '在['+RainyDice.group[Group_Platform][Group_ID]['Group_Name']+']('+str(Group_ID)+')中，'+ reply
        plugin_event.send('private',User_ID,reply)
        reply_grp = RainyDice.GlobalVal.GlobalMsg['rhGroupReply']
        user_name = RainyDice.user[Group_Platform][User_ID]['U_Name']
        reply_grp = str.replace(reply_grp,'[User_Name]',user_name)
        plugin_event.reply(reply_grp)
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
        if message == 'st':
            plugin_event.reply(RainyDice.GlobalVal.getHelpDoc('st'))
        else:
            message=str.strip(message[2:])
            status,isMultiReply ,reply = rd.ST(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
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
    elif message.startswith('r'):
        if len(message) == 1:
            message = 'r1d100'
        message=message[1:]
        status,isMultiReply ,reply = rd.RD(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
        plugin_event.reply(reply)
        return 1
    elif message.startswith('nn'):
        if message == 'nn':
            plugin_event.reply(RainyDice.GlobalVal.getHelpDoc('nn'))
        else:
            message=str.strip(message[2:])
            name = str.strip(message)
            RainyDice.user.set('U_Name',name,Group_Platform,User_ID)
            reply = RainyDice.GlobalVal.GlobalMsg['nnReply']
            # 'nnReply' : '已将[User_Name]的用户名称改为：[New_Name]'
            reply =str.replace(reply,'[User_Name]',plugin_event.data.sender['nickname'])
            reply =str.replace(reply,'[New_Name]',name)
            plugin_event.reply(reply)
        return 1
    elif message.startswith('li'):
        status,isMultiReply ,reply = rd.LI()
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
    elif message.startswith('ti'):
        status,isMultiReply ,reply = rd.TI()
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
    elif message.startswith('setcoc'):
        if message == 'setcoc':
            plugin_event.reply(RainyDice.GlobalVal.getHelpDoc('setcoc'))
        else:
            message=str.strip(message[6:])
            status,isMultiReply ,reply = rd.SETCOC(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
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
    elif message.startswith('en'):
        if message == 'en':
            plugin_event.reply(RainyDice.GlobalVal.getHelpDoc('en'))
        else:
            message=str.strip(message[2:])
            status,isMultiReply ,reply = rd.EN(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID)
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
    elif message.startswith('master'):
        pass
    elif message.startswith('admin'):
        pass
    elif message.startswith('log'):
        pass
    elif message.startswith('help'):
        pass
    else:
        return None
    
