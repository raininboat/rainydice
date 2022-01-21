# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  /
    /_/|_/_/ |_/___/_/|_/   /_/

    RainyDice 跑团投掷机器人服务 by RainyZhou
    消息发送基本模块

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

from rainydice.dice_command import chat_log
import OlivOS
import time

class Message_Send_All(object):
    def __init__(self,RainyDice,plugin_event=None,proc=None,flag_proc_log=True,flag_chat_log=False):
        self.RainyDice = RainyDice
        self.plugin_event = plugin_event
        self.proc = proc
        self.flag_proc_log = flag_proc_log
        self.flag_chat_log = flag_chat_log
        self.sendlist = []
        self.replylist = []
        self.data = Msg_Data_Basic(plugin_event=plugin_event,proc=proc,RainyDice=RainyDice)

    def attachMany(self,sendObjList):
        for sendObj in sendObjList:
            self.attach(sendObj)
    def attach(self,sendObj):
        if type(sendObj) is tuple:
            for i in sendObj:
                self.attach(i)
        else:
            if sendObj.flag_chat_log == None:
                sendObj.flag_chat_log = self.flag_chat_log
            if sendObj.type == 'send':
                self.sendlist.append(sendObj)
            elif sendObj.type == 'reply':
                self.replylist.append(sendObj)
            else:
                raise TypeError('sendObj type err: ' + sendObj.__class__.__name__)

    def clear(self):
        del self.sendlist , self.replylist
        self.sendlist = []
        self.replylist = []
        return True

    def send(self):
        # 消息发送，需要先使用attach将对应消息块加入消息回复暂存区中
        # 发送部分（私聊信息or其他平台）
        for thisMsg in self.sendlist:
            tmpfmtdict = self.data.fmtdata.copy()
            tmpfmtdict.update(thisMsg.formatDict)
            sendmsg = thisMsg.datastr.format_map(tmpfmtdict)
            thisMsgSendList = str.split(sendmsg,'\f')
            for msg in thisMsgSendList:
                self.plugin_event.send(thisMsg.send_type,thisMsg.target_id,msg)
                if self.flag_proc_log:
                    self.proc.log(0,'[RainyDice] send['+str(thisMsg.platform)+']['+thisMsg.send_type+']('+str(thisMsg.target_id)+') - '+msg)
                if thisMsg.flag_chat_log:
                    pass
                    # 私聊的 chat_log 先不做

        # 直接回复部分
        for thisMsg in self.replylist:
            tmpfmtdict = self.data.fmtdata.copy()
            tmpfmtdict.update(thisMsg.formatDict)
            sendmsg = thisMsg.datastr.format_map(tmpfmtdict)
            thisMsgSendList = str.split(sendmsg,'\f')
            for msg in thisMsgSendList:
                self.plugin_event.reply(msg)
                if self.flag_proc_log:
                    self.proc.log(0,'[RainyDice] reply - '+msg)
                # 查看plugin event 类型，如果不是群聊消息则一律忽略 chat_log
                # if self.data.func_type == 2:
                # 记录log消息
                if thisMsg.flag_chat_log and self.data.fmtdata['group_id'] != -1:
                    if 0 in dict.keys(self.RainyDice.group[self.data.platform_id][self.data.fmtdata['group_id']]['log']):
                        log_name = self.RainyDice.group[self.data.platform_id][self.data.fmtdata['group_id']]['log'][0]
                    else:
                        log_name = 'log_{0:d}_{1:d}_{2:d}'.format(self.data.platform_id,self.data.fmtdata['group_id'],time.time().__int__())
                        self.RainyDice.group.set('log',(0,log_name),self.data.platform_id,self.data.fmtdata['group_id'])
                        chat_log.log_create(self.RainyDice.bot,log_name)
                    # log记录
                    chat_log.log_msg(
                        self.RainyDice.bot,
                        log_name=log_name,
                        platform=self.data.platform_id,
                        user_id=self.data.fmtdata['self_id'],
                        user_name=self.data.fmtdata['self_name'],
                        user_text=msg,
                        log_time=time.time().__int__(),
                        group_id=self.data.fmtdata['group_id'],
                        group_name=self.RainyDice.group[self.data.platform_id][self.data.fmtdata['group_id']]['Group_Name']
                    )
        # 清空暂存区所有已经发送的内容
        self.clear()

class Msg_Data_Basic(object):
    def __init__(self,plugin_event,proc,RainyDice):
        self.self_id = plugin_event.base_info['self_id']
        self.platform = plugin_event.platform['platform']
        self.platform_id = RainyDice.platform_dict[self.platform]
        self.fmtdata = {
            'FormFeed' : '\f',
            'self_id' : self.self_id,
            'self_name' : '本机器人',
            'at' : '[at]',          # at 事件发送者
            'nick' : '用户昵称',
            'name' : '用户当前名称',
            'user_id' : -1,
            'group_id' : -1,
        }
        self.func_type = None
        # 判断插件事件类型（基本信息）
        if plugin_event.plugin_info['func_type'] in ('private_message',):
            # 私聊消息
            self.fmtdata['user_id'] = plugin_event.data.user_id
            self.func_type = 0
        elif plugin_event.plugin_info['func_type'] in ('group_message',):
            # 群聊消息
            self.fmtdata['user_id'] = plugin_event.data.user_id
            self.fmtdata['group_id'] = plugin_event.data.group_id
            self.func_type = 1
        elif plugin_event.plugin_info['func_type'] in ('friend_add','private_message_recall','friend_add_request'):
            # 好友相关其他消息or私聊其他信息
            self.fmtdata['user_id'] = plugin_event.data.user_id
            self.func_type = 2
        elif plugin_event.plugin_info['func_type'] in ('group_file_upload','group_admin','group_member_decrease','group_member_increase','group_ban','group_message_recall','poke','group_lucky_king','group_honor','group_add_request','group_invite_request'):
            # 群聊其他消息
            self.fmtdata['user_id'] = plugin_event.data.user_id
            self.fmtdata['group_id'] = plugin_event.data.group_id
            self.func_type = 3
        else:       # lifespan heartbeat
            # 框架消息
            self.func_type = 4
        # 根据插件事件类型进行fmt初始化
        self.fmtdata['self_name'] = RainyDice.bot.data['name']
        if self.func_type < 4:
            self.fmtdata['at'] = OlivOS.OlivOS.messageAPI.PARA.at(plugin_event.data.user_id).CQ()
        if self.func_type < 2:
            self.fmtdata['nick'] = plugin_event.data.sender['nickname']
        if self.fmtdata['user_id'] in RainyDice.user[self.platform_id]['user_list']:
            self.fmtdata['name'] = RainyDice.user[self.platform_id][self.fmtdata['user_id']]['U_Name']

class Msg_Send(object):
    def __init__(self,textRaw:str,formatDict={},platform=0,send_type='private',target_id=0,flag_chat_log=None):
        self.data = []
        self.datastr = ''
        self.type = 'send'
        self.send_type = send_type
        self.datastr = textRaw
        self.platform = platform
        self.target_id = target_id
        self.flag_chat_log = flag_chat_log
        self.formatDict = formatDict
    def extend(self,textRaw:str,formatDict={},reverse=False,flag_chat_log=None):
        if flag_chat_log != None:
            self.flag_chat_log = flag_chat_log
        if reverse:
            self.datastr = textRaw+self.datastr
            self.formatDict.update(formatDict)
            # self.formatDict=formatDict.update(self.formatDict)
        else:
            self.datastr = self.datastr+textRaw
            print(self.formatDict)
            self.formatDict.update(formatDict)

class Msg_Reply(object):
    def __init__(self,textRaw:str,formatDict={},flag_chat_log=None,**otherstastus):
        self.data = []
        self.datastr = textRaw
        self.type = 'reply'
        self.send_type = 'reply'
        self.formatDict = formatDict
        self.flag_chat_log = flag_chat_log
    def extend(self,textRaw:str,formatDict={},reverse=False,flag_chat_log=None):
        if flag_chat_log != None:
            self.flag_chat_log = flag_chat_log
        if reverse:
            self.datastr = textRaw+self.datastr
            self.formatDict.update(formatDict)
            # self.formatDict=formatDict.update(self.formatDict)
        else:
            self.datastr = self.datastr+textRaw
            print(self.formatDict)
            self.formatDict.update(formatDict)

def log_cmd(msg_obj:Message_Send_All,RainyDice,message:str,user_id:int,platform:int,group_id = 0):
    if message.startswith('on'):
        # log on 开始记录（创建表格）
        if RainyDice.group[platform][group_id]['isLogOn']:
            msg_obj.attach(Msg_Reply(RainyDice.GlobalVal.GlobalMsg['logAlreadyOn']))
            msg_obj.send()
            return None
        RainyDice.group.set('isLogOn',True,platform,group_id)
        if 0 in dict.keys(RainyDice.group[platform][group_id]['log']):
            log_name = RainyDice.group[platform][group_id]['log'][0]
        else:
            log_name = 'log_{0:d}_{1:d}_{2:d}'.format(platform,group_id,time.time().__int__())
            RainyDice.group.set('log',(0,log_name),platform,group_id)
            chat_log.log_create(RainyDice.bot,log_name)
        reply= RainyDice.GlobalVal.GlobalMsg['logOnReply']
        msg_obj.attach(Msg_Reply(reply,flag_chat_log=True))
        msg_obj.send()
        return None
    elif message.startswith('off'):
        # log off 暂停记录
        if not RainyDice.group[platform][group_id]['isLogOn']:
            reply = RainyDice.GlobalVal.GlobalMsg['logAlreadyOff']
            msg_obj.attach(Msg_Reply(reply))
            msg_obj.send()
            return None
        RainyDice.group.set('isLogOn',False,platform,group_id)
        reply= RainyDice.GlobalVal.GlobalMsg['logOffReply']
        msg_obj.attach(Msg_Reply(reply))
        msg_obj.send()
        return None
    elif message.startswith('end'):
        # log end 关闭记录(删除表格)并输出
        if not RainyDice.group[platform][group_id]['isLogOn']:
            reply = RainyDice.GlobalVal.GlobalMsg['logAlreadyOff']
            if 0 in dict.keys(RainyDice.group[platform][group_id]['log']):
                RainyDice.group.del_conf('log',0,platform,group_id)
            msg_obj.attach(Msg_Reply(reply))
            msg_obj.send()
            return None
        log_name = RainyDice.group[platform][group_id]['log'][0]
        reply = Msg_Reply('跑团记录已结束！正在生成记录文件 {file_name} ...',{'file_name':log_name})
        msg_obj.attach(reply)
        msg_obj.send()
        RainyDice.group.del_conf('log',0,platform,group_id)
        RainyDice.group.set('isLogOn',False,platform,group_id)
        status,log_path = chat_log.log_end(RainyDice.bot,log_name)
        reply = Msg_Reply('文件生成成功！',flag_chat_log= False)
        if status:
            if RainyDice.bot.data['email']['enabled']:
                if platform == 0:
                    receiver = [(RainyDice.user[platform][user_id]['U_Name'],str(user_id)+"@qq.com")]
                    reply.extend('正在发送邮件至邮箱: {email_addr}',formatDict={'email_addr' : str(user_id)+"@qq.com"})
                    msg_obj.attach(reply)
                    msg_obj.send()
                    status = chat_log.log_email.send_email(RainyDice.bot.data,log_path,receiver)
                    if status:
                        reply = Msg_Reply('发送log至邮箱成功！请前往发送者账号的qq邮箱获取（如果找不到就去垃圾邮件中寻找）',flag_chat_log=False)
                        msg_obj.attach(reply)
                    else:
                        reply = Msg_Reply('发送log至邮箱失败！请联系管理员获取log！\n文件：{log_path}*.*',{'log_path' : log_path},flag_chat_log=False)
                        msg_obj.attach(reply)
                else:
                    reply.extend('未完成qq以外平台的email发送，请联系管理员获取log！\n文件：{log_path}*.*',{'log_path' : log_path},flag_chat_log=False)
                    msg_obj.attach(reply)
            else:
                reply.extend('email发送模块关闭，请联系管理员获取log！\n文件：'+log_path+'*.*',{'log_path' : log_path},flag_chat_log=False)
                msg_obj.attach(reply)
            # reply= RainyDice.GlobalVal.GlobalMsg['logEndReply']
        else:
            reply = Msg_Reply(log_path,flag_chat_log=False)
            msg_obj.attach(reply)
        msg_obj.send()
        return None
    else:
        msg_obj.attach(Msg_Reply('请检查指令'))
        msg_obj.send()
        return None
