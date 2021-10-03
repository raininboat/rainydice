# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  / 
    /_/|_/_/ |_/___/_/|_/   /_/  

    RainyDice 跑团投掷机器人服务 by RainyZhou
        log 模块

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

import time
import sqlite3
import os

from rainydice.dice_command import log_email,log_render
from rainydice.msgesacpe import messageEscape

# def __init__(self,Data_path,log,bot):
#     self.sql_path = Data_path + '/RainyDice.db'
#     self.log_path = Data_path + '/log/'
#     self.proc_log = log
#     self.logconf = bot.data['log']
class _log_conf(object):
    def __init__(self,bot):
        self.proc_log = bot.log
        Data_path = bot.Data_Path
        self.sql_path = Data_path + '/RainyDice.db'
        self.log_path = Data_path + '/log/'
        self.logconf = bot.data['log']

def log_name_create(platform,group_id):
    log_name = 'log_{0:d}_{1:d}_{2:d}'.format(platform,group_id,time.time())
    return log_name
def log_create(botinfo,log_name):
    self = _log_conf(botinfo)
    SQL_conn = sqlite3.Connection(self.sql_path)
    cur = SQL_conn.cursor()
    try:
        pre_sql = '''CREATE TABLE IF NOT EXISTS {log_name}(
    'ID'    INTEGER PRIMARY KEY   AUTOINCREMENT,
    'Platform'      integer         NOT NULL,
    'User_ID'       integer         default 0,
    'User_Name'     TEXT            default '用户',
    'User_Text'     TEXT            default '',
    'Log_Time'      integer         default 0,
    'Group_ID'       integer        default 0,
    'Group_Name'     TEXT           default '群聊'
);'''.format(log_name=log_name)
        cur.execute(pre_sql)
        SQL_conn.commit()
    except sqlite3.Error as err:
        self.proc_log(3,'log create失败！sql: '+pre_sql+' ; err: '+err.__str__())
        SQL_conn.rollback()
    finally:
        cur.close()
        SQL_conn.close()
    self.proc_log(0,'Created Log Form: '+log_name)

def log_msg(botinfo,log_name,platform,user_id,user_name,user_text,log_time,group_id=0,group_name='群聊'):
    self = _log_conf(botinfo)
    SQL_conn = sqlite3.Connection(self.sql_path)
    cur = SQL_conn.cursor()
    pre_sql = '''INSERT INTO {log_name}('Platform','User_ID','User_Name','User_Text','Log_Time','Group_ID','Group_Name')
    VALUES (?,?,?,?,?,?,?);'''.format(log_name=log_name)
    user_text = messageEscape.escape_before_save(messageEscape.cqcode_replace(user_text),False)
    try:
        cur.execute(pre_sql,(platform,user_id,user_name,user_text,log_time,group_id,group_name))
        SQL_conn.commit()
        # self.proc_log(0,'logging！sql: '+pre_sql+' ; val: '+(platform,user_id,user_name,user_text,log_time,group_id,group_name).__str__())
    except sqlite3.Error as err:
        self.proc_log(3,'log失败！sql: '+pre_sql+' ; err: '+err.__str__())
        SQL_conn.rollback()
    finally:
        cur.close()
        SQL_conn.close()

def log_end(botinfo,log_name):
    self = _log_conf(botinfo)
    SQL_conn = sqlite3.Connection(self.sql_path)
    cur = SQL_conn.cursor()
    pre_sql = '''SELECT * FROM {log_name}'''.format(log_name=log_name)
    log_path = self.log_path+log_name+'/'
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    if self.logconf['csv']:
        log_csv = log_render.LogCsv(log_path)
    if self.logconf['html']:
        log_html = log_render.LogHtml(log_path)
    if self.logconf['doc']:
        log_doc = log_render.LogDocx(log_path)
    log_txtRaw = log_render.LogTxtRaw(log_path)

    try:
        cur.execute(pre_sql)
        temp = cur.fetchall()
        # print(temp)
        if temp != []:
            user_list = []
            for line in temp:
                thisline=log_render.LogLine(line)
                if thisline.id in user_list:
                    color_id=user_list.index(thisline.id)
                else:
                    color_id = len(user_list)
                    user_list.append(thisline.id)
                if self.logconf['csv']:
                    log_csv.logline(thisline,color_id)
                if self.logconf['html']:
                    log_html.logline(thisline,color_id)
                if self.logconf['doc']:
                    log_doc.logline(thisline,color_id)
                log_txtRaw.logline(thisline,color_id)
            pre_sql = '''DROP TABLE {log_name}'''.format(log_name=log_name)
            cur.execute(pre_sql)
            SQL_conn.commit()
            status = True
    except sqlite3.Error as err:
        self.proc_log(3,'log end失败！sql: '+pre_sql+' ; err: '+err.__str__())
        SQL_conn.rollback()
        status = False
        log_path = 'log end失败！err: '+err.__str__()
    finally:
        if self.logconf['csv']:
            log_csv.logsave()
        if self.logconf['html']:
            log_html.logsave()
        if self.logconf['doc']:
            log_doc.logsave()
        log_txtRaw.logsave()
        cur.close()
        SQL_conn.close()
    return status,log_path


def log_cmd(plugin_event,Proc,RainyDice,message:str,user_id:int,platform:int,group_id = 0):
    if message.startswith('on'):
        # log on 开始记录（创建表格）
        if RainyDice.group[platform][group_id]['isLogOn']:
            reply = RainyDice.GlobalVal.GlobalMsg['logAlreadyOn']
            return 0,False,reply,True
        RainyDice.group.set('isLogOn',True,platform,group_id)
        if 0 in dict.keys(RainyDice.group[platform][group_id]['log']):
            log_name = RainyDice.group[platform][group_id]['log'][0]
        else:
            log_name = 'log_{0:d}_{1:d}_{2:d}'.format(platform,group_id,time.time().__int__())
            RainyDice.group.set('log',(0,log_name),platform,group_id)
            log_create(RainyDice.bot,log_name)
        reply= RainyDice.GlobalVal.GlobalMsg['logOnReply']
        return 0,False,reply,True
    elif message.startswith('off'):
        # log off 暂停记录
        if not RainyDice.group[platform][group_id]['isLogOn']:
            reply = RainyDice.GlobalVal.GlobalMsg['logAlreadyOff']
            return 0,False,reply,False
        RainyDice.group.set('isLogOn',False,platform,group_id)
        reply= RainyDice.GlobalVal.GlobalMsg['logOffReply']
        return 0,False,reply,False
    elif message.startswith('end'):
        # log end 关闭记录(删除表格)并输出
        if not RainyDice.group[platform][group_id]['isLogOn']:
            reply = RainyDice.GlobalVal.GlobalMsg['logAlreadyOff']
            if 0 in dict.keys(RainyDice.group[platform][group_id]['log']):
                RainyDice.group.del_conf('log',0,platform,group_id)
        log_name = RainyDice.group[platform][group_id]['log'][0]
        RainyDice.group.del_conf('log',0,platform,group_id)
        RainyDice.group.set('isLogOn',False,platform,group_id)
        status,log_path = log_end(RainyDice.bot,log_name)
        if status:
            if RainyDice.bot.data['email']['enabled']:
                if platform == 0:
                    receiver = [(RainyDice.user[platform][user_id]['U_Name'],str(user_id)+"@qq.com")]
                    status = log_email.send_email(RainyDice.bot.data,log_path,receiver)
                    if status:
                        reply = '发送log至邮箱成功！请前往发送者账号的qq邮箱获取（如果找不到就去垃圾邮件中寻找）'
                    else:
                        reply = '发送log至邮箱失败！请联系管理员获取log！\n文件：'+log_path+'*.*'
                else:
                    reply = '未完成qq以外平台的email发送，请联系管理员获取log！\n文件：'+log_path+'*.*'
            else:
                reply = 'email发送模块关闭，请联系管理员获取log！\n文件：'+log_path+'*.*'
            
            # reply= RainyDice.GlobalVal.GlobalMsg['logEndReply']
        else:
            reply = log_path
        return 0,False,reply,False
    else:
        return 0,False,'请检查指令',True