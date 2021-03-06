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

from rainydice.dice_command import log_email,log_render,message_send
from rainydice.msgesacpe import messageEscape

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

def send_reply(plugin_event,proc,reply,RainyDice,isLogOn=False,isMultiReply=False,status=0,Group_Platform=0,Group_ID=0):
    '【已弃用】 回复消息请使用 dice_command.message_send 进行构造发送'
    if isMultiReply:
        for replypack in reply:
            if replypack[0] == 'reply':
                msglst = str.split(replypack[1],'\f')
                for msg in msglst:
                    proc.log(0,'[RainyDice]reply:'+msg)
                    plugin_event.reply(msg)
            elif replypack[0] == 'send':
                target_type = replypack[1]
                target_id = replypack[2]
                # reply_msg = replypack[3]
                msglst = str.split(replypack[3],'\f')
                for msg in msglst:
                    proc.log(0,'[RainyDice]send['+target_type+']('+str(target_id)+'):'+msg)
                    plugin_event.send(target_type,target_id,msg)
    else:
        msglst = str.split(reply,'\f')
        for msg in msglst:
            proc.log(0,'[RainyDice]reply:'+msg)
            plugin_event.reply(msg)
    if isLogOn and Group_ID != 0:
        log_name = RainyDice.group[Group_Platform][Group_ID]['log'][0]
        if 0 in dict.keys(RainyDice.group[Group_Platform][Group_ID]['log']):
            log_name = RainyDice.group[Group_Platform][Group_ID]['log'][0]
        else:
            log_name = 'log_{0:d}_{1:d}_{2:d}'.format(Group_Platform,Group_ID,time.time().__int__())
            RainyDice.group.set('log',(0,log_name),Group_Platform,Group_ID)
            log_create(RainyDice.bot,log_name)
        log_name = RainyDice.group[Group_Platform][Group_ID]['log'][0]
        group_name = RainyDice.group[Group_Platform][Group_ID]['Group_Name']
        self_id = plugin_event.base_info['self_id']
        self_name = RainyDice.bot.data['name']
        if isMultiReply:
            for replypack in reply:
                if replypack[0] == 'reply':
                    msglst = str.split(replypack[1],'\f')
                    for msg in msglst:
                        proc.log(0,'[RainyDice]logging:'+msg)
                        log_msg(RainyDice.bot,log_name=log_name,platform=Group_Platform,user_id=self_id,user_name=self_name,user_text=msg,log_time=time.time().__int__(),group_id=Group_ID,group_name=group_name)
        else:
            msglst = str.split(reply,'\f')
            for msg in msglst:
                proc.log(0,'[RainyDice]logging:'+msg)
                log_msg(RainyDice.bot,log_name=log_name,platform=Group_Platform,user_id=self_id,user_name=self_name,user_text=msg,log_time=time.time().__int__(),group_id=Group_ID,group_name=group_name)
