# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  /
    /_/|_/_/ |_/___/_/|_/   /_/

    RainyDice 跑团投掷机器人服务 by RainyZhou
        存储类

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
from OlivOS.infoAPI import OlivOS_Version
PLATFORM_VERSION_LEAST = '0.6.0'
from rainydice import GlobalVal
from rainydice import RainyDice_Version as version,RainyDice_Author as author
from rainydice.msgesacpe import messageEscape
from rainydice.dice_command import public_deck
import rainydice.versionAdapter as versionAdapter
# from rainydice.main import RainyDice
#from data.rainydice import *
import json
import sqlite3
import time
import os
class Dice(object):
    def __init__(self,Data_Path,log,cocRankCheck,ignore={}):
        self.platform_dict = {
            'qq' : 0,
            'telegram' : 1,
            "dodo" : 2
        }
        self.platform_list = ['qq','telegram',"dodo"]
        self.sql_path = Data_Path + '/RainyDice.db'
        self.data_path = Data_Path
        self.log = log
        self.basic = basic_info(Data_Path,log = log)
        self.ignore = ignore
        self.cocRankCheck = cocRankCheck
        self.bot = bot(Data_Path,log = log)
        self.group = Group(sql_path=self.sql_path,log = log)
        self.user = User(sql_path=self.sql_path,log = log)  # 用户信息先不读取，在开始使用时再进行读取
        self.GlobalVal = GlobalVal.GlobalVal(cocrank=cocRankCheck)
        self.starttime = time.time()
        self.publicDeck = deckload(Data_Path,log)

    def check_user_trust(self,userid,platform):
        '获取某一用户的信任度'
        if userid == self.bot.data[self.platform_list[platform]+'_master']:
            if self.user[platform][userid]['U_Trust'] < 255:
                self.user.set('U_Trust',255,platform,userid)
                self.log(2,'将用户[{0}][{1}]的信任设为255 (master)'.format(platform,userid))
            return 255
        elif userid in self.bot.data[self.platform_list[platform]+'_admin']:
            if self.user[platform][userid]['U_Trust'] < 4:
                self.user.set('U_Trust',4,platform,userid)
                self.log(2,'将用户[{0}][{1}]的信任设为4 (admin)'.format(platform,userid))
            return 4
        else:
            return self.user[platform][userid]['U_Trust']

class deckload(object):
    def __init__(self,datapath,log):
        self.data_path = datapath
        self.log = log
        keys,skip,info = public_deck.initPublicDeck(datapath)
        self.decks = keys
        self.metaInfo = info
        self.skip = skip

class basic_info(object):
    def __init__(self,path,log):
        ovo_version = versionAdapter.diceversion(OlivOS_Version)
        if ovo_version.lessthan(0,5,0):
            raise UserWarning('当前 OlivOS 版本过旧: {0}，RainyDice需求最低框架版本为{1}')
        sql_path = path + '/RainyDice.db'
        SQL_conn = SQL(sql_path)
        pre_sql = '''CREATE TABLE IF NOT EXISTS basic_info( 'basic_key' Text primary key NOT NULL UNIQUE ,'basic_val' text);'''
        SQL_conn.cursor.execute(pre_sql)
        pre_sql = '''SELECT * FROM basic_info;'''
        SQL_conn.cursor.execute(pre_sql)
        temp = SQL_conn.cursor.fetchall()
        if temp == []:
            pre_sql = '''INSERT INTO basic_info ('basic_key','basic_val') VALUES (?,?),(?,?),(?,?);'''
            val = ('version',version,'author',author,'create_time',time.time())
            SQL_conn.cursor.execute(pre_sql,val)
            SQL_conn.connection.commit()
            self.version = versionAdapter.diceversion(version)
        else:
            data = {}
            for i in temp:
                data[i[0]] = i[1]
            if 'version' not in data:
                data['version'] = '0.0.0-unknown'
            self.version = versionAdapter.diceversion(data['version'])
            self.author = data['author']
            self.create_time = data['create_time']
        self.sql_path = sql_path
        if self.version.fullversion != version:
            status= versionAdapter.version_updater(path,self.version.fullversion,log)
            if status:
                self.version=versionAdapter.diceversion(version)
            else:
                raise UserWarning('RainyDice版本升级错误！脚本版本: '+version+'，存档版本: '+self.version.fullversion)

class bot(object):
    def __init__(self,Data_Path,log):
        self.log = log
        self.Data_Path = Data_Path
        try:
            f = open(Data_Path+'/conf/bot.json', 'r', encoding = 'utf-8')
            bot_conf = json.loads(f.read())
            f.close()
            log(0,'已读取RainyDice配置文件 bot.json')
        except:
            log(2,'未找到RainyDice配置文件 bot.json ，即将新建...')
            log(2,'请前往 plugin/data/rainydicr/conf 中进一步修改 bot.json')
            bot_conf = self.create_bot_conf(Data_Path,log)
        finally:
            if bot_conf == None:
                log(3,'RainyDice配置文件 bot.json 错误！即将重置...')
                log(2,'请前往 plugin/data/rainydicr/conf 中进一步修改 bot.json')
                bot_conf = self.create_bot_conf(Data_Path,log)
        self.data = bot_conf

        logconf = {
            'csv' : True,
            "html" : False,
            "doc" : True
        }
        emailconf = {
        "enabled" : False,
        "host" : "SMTP发送服务器，去不同服务商的文档中查看：e.g：smtp.exmail.qq.com",
        "port" : 465,
        "ssl" : True,
        "useraddr" : "具体邮箱名称：e.g: noreply@mail.rainydice.cn",
        "password" : "邮箱smtp客户端授权码：xxxxxxxxxxx"
    }
        ischanged = False
        if 'log' not in bot_conf.keys() or type(bot_conf['log']) != dict:
            self.data['log'] = logconf
            ischanged = True
        else:
            tmpkeys = self.data['log'].keys()
            for key in logconf.keys():
                if key not in tmpkeys:
                    self.data['log'][key] = logconf[key]
                    ischanged = True
        if 'email' not in bot_conf.keys() or type(bot_conf['email']) != dict:
            self.data['email'] = emailconf
            ischanged = True
            log(2,'请前往 plugin/data/rainydicr/conf 中进一步修改 bot.json 完成 email 适配')
        else:
            tmpkeys = self.data['email'].keys()
            for key in emailconf.keys():
                if key not in tmpkeys:
                    self.data['email'][key] = logconf[key]
                    log(2,'请前往 plugin/data/rainydicr/conf 中进一步修改 bot.json 完成 email 适配')
                    ischanged = True
        if ischanged:
            self.set()

    def create_bot_conf(self,Data_Path= '',log=None):
        f_conf = open(Data_Path+'/conf/bot.json',"w",encoding="utf-8")
        default_conf = '''\
{
    "email":{
        "enabled" : false,
        "host" : "SMTP发送服务器，去不同服务商的文档中查看：e.g：smtp.exmail.qq.com",
        "port" : 465,
        "ssl" : true,
        "useraddr" : "具体邮箱名称：e.g: noreply@mail.rainydice.cn",
        "password" : "邮箱smtp客户端授权码：xxxxxxxxxxx"
    },
    "log": {
        "csv": false,
        "doc": true,
        "html": false
    },
    "name": "本机器人",
    "qq_admin": [
        0
    ],
    "qq_master": 0,
    "telegram_admin": [
        0
    ],
    "telegram_master": 0
}
'''
        f_conf.write(default_conf)
        f_conf.close()
        conf = {
    "email":{
        "enabled" : False,
        "host" : "SMTP发送服务器，去不同服务商的文档中查看：e.g：smtp.exmail.qq.com",
        "port" : 465,
        "ssl" : True,
        "useraddr" : "具体邮箱名称：e.g: noreply@mail.rainydice.cn",
        "password" : "邮箱smtp客户端授权码：xxxxxxxxxxx"
    },
    "log": {
        "csv": False,
        "doc": True,
        "html" : False
    },
    "name": "本机器人",
    "qq_admin": [
        0
    ],
    "qq_master": 0,
    "telegram_admin": [
        0
    ],
    "telegram_master": 0
}
        return conf

    def set(self, key=None, value=None):      # 设置bot属性一律用这个(可以进行连接同步)，读取属性可以直接看 self.data['key'] admin等json数据除外
        '''
        存储属性至json中，
        key + val填写则自动添加这一键值对（用于适配以前sql的用法）
        '''
        if key != None:
            self.data[key] = value
        data = self.data
        s_json = json.dumps(data,ensure_ascii=False,indent='    ',sort_keys=True)
        f_conf = open(self.Data_Path+'/conf/bot.json',"w",encoding="utf-8")
        f_conf.write(s_json)
        f_conf.close()
        return True

class SQL(object):
    def __init__(self,Path):
        self.connection = sqlite3.connect(Path)
        self.cursor = self.connection.cursor()
        self.path = Path
    def __del__(self):
        self.cursor.close()
        self.connection.close()

class Group(dict):
    def __init__(self,sql_path,log):
        self.log = log
        SQL_conn = SQL(sql_path)
        platform_number = [0,1,2]         # 所有platform的数字
        # 所有键名称
        self.key = ('Group_Platform','Group_ID','Group_Setcoc','Group_Name','Group_Owner','Group_Status','Group_Trust')
        #self.jsonconf = ['Group_Setcoc','admin']
        self.singleconf = ['card','admin','name','log']
        self.statusconf = ['isBotOn','isPluginOn','isLogOn','isBanRecall']
        # platform 为群组出自平台，qq 为 0，tg 为 1
        pre_sql = '''CREATE TABLE IF NOT EXISTS GROUP_CONF(
    'Group_Platform'          integer              NOT NULL,
    'Group_ID'              integer           NOT NULL,
    'Group_Setcoc'             integer        default 0,
    'Group_Name'              TEXT            default '群聊',
    'Group_Owner'             integer         default 0,
    'Group_Status'       integer         default 3,
    "Group_Trust"             integer         default 0,
    PRIMARY KEY('Group_Platform','Group_ID')
);'''
        SQL_conn.cursor.execute(pre_sql)
        pre_sql = '''SELECT * FROM GROUP_CONF;'''
        SQL_conn.cursor.execute(pre_sql)
        temp = SQL_conn.cursor.fetchall()
        # print (temp)
        for i in platform_number:   # 初始化每个平台的字典
            self[i] = {}
            self[i]['group_list'] = list()
        if not temp == []:
            for group_temp_val in temp:      # 单个群组
                self[group_temp_val[0]][group_temp_val[1]] = {}     # Group[平台][群号][属性]
                self[group_temp_val[0]]['group_list'].append(group_temp_val[1])
                for i in range(len(self.key)):
                    self[group_temp_val[0]][group_temp_val[1]][self.key[i]] = group_temp_val[i]
                b_status = self[group_temp_val[0]][group_temp_val[1]]['Group_Status']
                status = self.__bintostatus(b_status)
                dict.update(self[group_temp_val[0]][group_temp_val[1]],status)
                # 读取单群信息
                pre_sql = '''CREATE TABLE IF NOT EXISTS group_{0}_{1}(
    'group_key'          TEXT              NOT NULL,
    'val_1'              integer           NOT NULL,
    'val_2'             Text            default 'default text',
    PRIMARY KEY('group_key','val_1')
);'''.format(str(group_temp_val[0]),str(group_temp_val[1]))
                #print(pre_sql)
                SQL_conn.cursor.execute(pre_sql)
                pre_sql = '''SELECT * FROM group_{0:d}_{1:d};'''.format(group_temp_val[0],group_temp_val[1])
                SQL_conn.cursor.execute(pre_sql)
                SQL_conn.connection.commit()
                for all_keys in self.singleconf:
                    self[group_temp_val[0]][group_temp_val[1]][all_keys] = {}
                this_group = SQL_conn.cursor.fetchall()
                if this_group != []:
                    for this_key in this_group:
                        self[group_temp_val[0]][group_temp_val[1]][this_key[0]][this_key[1]] = this_key[2]
                # self[group_temp_val[0]][group_temp_val[1]] = json.loads(s_json)
        SQL_conn.cursor.close()
        self.sql_path = sql_path
    # 将二进制存储的group_status转换为标准形式
    def __bintostatus(self,b_status):
        status = {}
        for i in range(len(self.statusconf)):
            thisbit = b_status&1<<i
            if thisbit:
                status[self.statusconf[i]]=True
            else:
                status[self.statusconf[i]]=False
        return status
    def __statustobin(self,groupdict):
        status = 0
        for i in range(len(self.statusconf)):
            thisbit = 0
            if groupdict[self.statusconf[i]]:
                thisbit = 1<<i
                status = status+thisbit
        return status
    def set(self, key, value,platform,group_id):      # 设置bot属性一律用这个(可以进行连接同步)，读取属性可以直接看 self.data['key']
        if key in self.singleconf:
            val_1 = value[0]
            val_2 = value[1]
            self[platform][group_id][key][val_1] = val_2
            sql_path = self.sql_path
            SQL_conn = SQL(sql_path)
            pre_sql = '''INSERT OR REPLACE INTO group_{0:d}_{1:d} ('group_key','val_1','val_2')
            VALUES(?,?,?)'''.format(platform,group_id)
            try:
                SQL_conn.cursor.execute(pre_sql,(key,val_1,val_2))
                SQL_conn.connection.commit()
                if SQL_conn.connection.total_changes == 0:
                    self.log(3,'未能更改数据库数据!')
                    # SQL_conn.write_sql(pre_sql,(value,key))
                    return False
                return True
            except Exception as err:
                self.log(4,'数据库错误，即将回滚!'+err.__str__())
                SQL_conn.connection.rollback()
                return False
        else:
            self[platform][group_id][key] = value
            groupdict = self[platform][group_id]
            Group_Status = self.__statustobin(groupdict)
            sql_path = self.sql_path
            SQL_conn = SQL(sql_path)
            pre_sql = '''INSERT OR REPLACE INTO GROUP_CONF ('Group_Platform','Group_ID','Group_Setcoc','Group_Name','Group_Owner','Group_Status','Group_Trust')
            VALUES(?,?,?,?,?,?,?);'''
            Group_Platform = self[platform][group_id]['Group_Platform']
            Group_Name = self[platform][group_id]['Group_Name']
            Group_Setcoc = self[platform][group_id]['Group_Setcoc']
            Group_ID = self[platform][group_id]['Group_ID']
            Group_Owner = self[platform][group_id]['Group_Owner']
            Group_Trust = self[platform][group_id]['Group_Trust']
            try:
                SQL_conn.cursor.execute(pre_sql,(Group_Platform,Group_ID,Group_Setcoc,Group_Name,Group_Owner,Group_Status,Group_Trust))
                SQL_conn.connection.commit()
                if SQL_conn.connection.total_changes == 0:
                    self.log(3,'未能更改数据库数据!')
                    # SQL_conn.write_sql(pre_sql,(value,key))
                    return False
                return True
            except Exception as err:
                self.log(4,'数据库错误，即将回滚!'+err.__str__())
                SQL_conn.connection.rollback()
                return False

    # 删除log记录
    def del_conf(self,key,val_1,platform,group_id):
        del self[platform][group_id][key][val_1]
        sql_path = self.sql_path
        SQL_conn = SQL(sql_path)
        pre_sql = '''DELETE FROM group_{platform:d}_{group_id:d} WHERE group_key glob {key} AND val_1 = {val_1}'''.format(platform=platform,group_id=group_id,key='"'+key+'"',val_1=val_1)
        try:
            SQL_conn.cursor.execute(pre_sql)
            SQL_conn.connection.commit()
            if SQL_conn.connection.total_changes == 0:
                self.log(3,'未能更改数据库数据!')
                # SQL_conn.write_sql(pre_sql,(value,key))
                return False
            return True
        except Exception as err:
            self.log(4,'数据库错误，即将回滚!'+err.__str__())
            SQL_conn.connection.rollback()
            return False

    # 添加新群组
    def add_group(self,Group_Platform,Group_ID,admin = [0],Group_Setcoc = 0,Group_Name = '群聊',Group_Owner=0,Group_Status = 3,Group_Trust = 0,isBotOn = True,isPluginOn = True,isLogOn = False):
        if Group_ID not in self[Group_Platform]['group_list']:
            self[Group_Platform]['group_list'].append(Group_ID)
        self[Group_Platform][Group_ID] = {
            'Group_Platform': Group_Platform,
            'Group_Name'    : Group_Name,
            'Group_ID'      : Group_ID,
            'Group_Owner'   : Group_Owner,
            #'Group_Status'  : Group_Status,
            'Group_Trust'   : Group_Trust,
            'admin'         : admin,
            'card' : {},
            'name' : {},
            'log'  : {},
            'Group_Setcoc'        : Group_Setcoc,
            'isBotOn'       : isBotOn,
            'isPluginOn'    : isPluginOn,
            'isLogOn'       : isLogOn,
            'isBanRecall'   : False
        }
        self[Group_Platform][Group_ID]['Group_Status'] = self.__statustobin(groupdict=self[Group_Platform][Group_ID])
        Group_Status = self[Group_Platform][Group_ID]['Group_Status']
        sql_path = self.sql_path
        SQL_conn = SQL(sql_path)
        pre_sql = '''INSERT OR REPLACE INTO GROUP_CONF ('Group_Platform','Group_ID','Group_Setcoc','Group_Name','Group_Owner','Group_Status','Group_Trust')
        VALUES(?,?,?,?,?,?,?);'''

        try:
            SQL_conn.cursor.execute(pre_sql,(Group_Platform,Group_ID,Group_Setcoc,Group_Name,Group_Owner,Group_Status,Group_Trust))
            pre_sql = '''CREATE TABLE IF NOT EXISTS group_{0:d}_{1:d}(
    'group_key'          TEXT              NOT NULL,
    'val_1'              integer           NOT NULL,
    'val_2'             Text            default 'default text',
    PRIMARY KEY('group_key','val_1')
);'''.format(Group_Platform,Group_ID)
            SQL_conn.cursor.execute(pre_sql)
            SQL_conn.connection.commit()
            if SQL_conn.connection.total_changes == 0:
                self.log(3,'未能更改数据库数据!')
                # SQL_conn.write_sql(pre_sql,(value,key))
                return False
            return True
        except Exception as err:
            self.log(4,'数据库错误，即将回滚!'+err.__str__())
            SQL_conn.connection.rollback()
            return False

class User(dict):
    def __init__(self,sql_path,log):
        self.log = log
        self.sql_path=sql_path
        self.platform_number = [0,1,2]         # 所有platform的数字
        # 所有键名称
        self.keyall = ('U_Platform','U_ID','U_Name','U_EnabledCard','U_Trust','U_CriticalSuccess','U_ExtremeSuccess','U_HardSuccess','U_RegularSuccess','U_Failure','U_Fumble')
        self.key = ('U_Platform','U_ID','U_Name','U_EnabledCard','U_Trust')
        self.card_key = ('Card_ID','Card_Name','Card_JSON')
        for i in self.platform_number:   # 初始化每个平台的字典
            self[i] = {}
            self[i]['user_list'] = list()
        SQL_conn = SQL(self.sql_path)
        self.jsonconf = []
        # platform 为群组出自平台，qq 为 0，tg 为 1
        pre_sql = '''CREATE TABLE IF NOT EXISTS USER_CONF(
    'U_Platform'          integer         NOT NULL,
    'U_ID'                integer         NOT NULL,
    'U_Name'              TEXT            default '用户',
    'U_EnabledCard'       integer         default 0,
    'U_Trust'             integer         default 0,
    'U_CriticalSuccess'   integer         default 0,
    'U_ExtremeSuccess'    integer         default 0,
    'U_HardSuccess'       integer         default 0,
    'U_RegularSuccess'    integer         default 0,
    'U_Failure'           integer         default 0,
    'U_Fumble'            integer         default 0,
    primary key ('U_Platform','U_ID')
);'''
        SQL_conn.cursor.execute(pre_sql)
        # pre_sql = '''SELECT * FROM USER_CONF;'''
        pre_sql = '''SELECT U_Platform,U_ID,U_Name,U_EnabledCard,U_Trust FROM USER_CONF;'''
        SQL_conn.cursor.execute(pre_sql)
        SQL_conn.connection.commit()
        temp = SQL_conn.cursor.fetchall()
        # print (temp)
        if not temp == []:
            for temp_val in temp:      # 单个群组
                self[temp_val[0]][temp_val[1]] = {}     # Group[平台][群号][属性]
                self[temp_val[0]]['user_list'].append(temp_val[1])
                for i in range(len(self.key)):
                    self[temp_val[0]][temp_val[1]][self.key[i]] = temp_val[i]
                # s_json = self[group_temp_val[0]][group_temp_val[1]]['Group_Setcoc']
                # self[group_temp_val[0]][group_temp_val[1]] = json.loads(s_json)
        SQL_conn.cursor.close()
        self.sql_path = sql_path
    # 添加新用户
    def add_user(self,U_Platform,U_ID,U_Name='用户',sender = {},U_EnabledCard=0,U_Trust=0): # ,U_CriticalSuccess=0,U_ExtremeSuccess=0,U_HardSuccess=0,U_RegularSuccess=0,U_Failure=0,U_Fumble=0):
        # 'sender': {'age': 0, 'area': '', 'card': '', 'level': '', 'nickname': 'xxx', 'role': 'owner', 'sex': 'unknown', 'title': '头衔', 'user_id': 1234567890},
        self.log(0,'adding user:['+str(U_Platform)+']('+str(U_ID)+')')
        if sender != {}:
            if U_Name == '用户':
                U_Name = sender['nickname']
        if U_ID not in self[U_Platform]['user_list']:
            self[U_Platform]['user_list'].append(U_ID)
        self[U_Platform][U_ID] = {
            'U_Platform' : U_Platform,
            'U_ID' : U_ID ,
            'U_Name' : U_Name,
            'U_EnabledCard' : U_EnabledCard,
            'U_Trust' : U_Trust,
            # 'U_CriticalSuccess' : U_CriticalSuccess,
            # 'U_ExtremeSuccess' : U_ExtremeSuccess,
            # 'U_HardSuccess' : U_HardSuccess,
            # 'U_RegularSuccess' : U_RegularSuccess,
            # 'U_Failure' : U_Failure,
            # 'U_Fumble' : U_Fumble
        }
        sql_path = self.sql_path
        SQL_conn = SQL(sql_path)

        try:
            #print('### trying to create tab')
            pre_sql =f''' CREATE TABLE IF NOT EXISTS user_%d_%d('user_key'  TEXT PRIMARY KEY NOT NULL , 'val_1' text, 'val_2' text);'''%(U_Platform,U_ID)
            SQL_conn.cursor.execute(pre_sql)
            #print('### trying to insert usercard')
            pre_sql =''' INSERT OR REPLACE INTO user_%d_%d('user_key','val_1','val_2') VALUES ('card-0','用户标准人物卡','{"_null" : -1}');'''%(U_Platform,U_ID)
            SQL_conn.cursor.execute(pre_sql)
            #print('### trying to insert user')
        #     pre_sql = '''INSERT OR REPLACE INTO USER_CONF ('U_Platform','U_ID','U_Name','U_EnabledCard','U_Trust','U_CriticalSuccess','U_ExtremeSuccess','U_HardSuccess','U_RegularSuccess','U_Failure','U_Fumble')
        # VALUES(?,?,?,?,?,?,?,?,?,?,?);'''
            pre_sql = '''INSERT OR REPLACE INTO USER_CONF ('U_Platform','U_ID','U_Name','U_EnabledCard','U_Trust')
        VALUES(?,?,?,?,?);'''
            # SQL_conn.cursor.execute(pre_sql,(U_Platform,U_ID,U_Name,U_EnabledCard,U_Trust,U_CriticalSuccess,U_ExtremeSuccess,U_HardSuccess,U_RegularSuccess,U_Failure,U_Fumble))
            SQL_conn.cursor.execute(pre_sql,(U_Platform,U_ID,U_Name,U_EnabledCard,U_Trust))
            #print('### trying to commit')
            SQL_conn.connection.commit()
            if SQL_conn.connection.total_changes == 0:
                self.log(3,'未能更改数据库数据!')
                # SQL_conn.write_sql(pre_sql,(value,key))
                return False
            return True
        except Exception as err:
            self.log(4,'数据库错误，即将回滚! err: ' +err.__str__())
            SQL_conn.connection.rollback()
            return False
    def set(self, key, value,platform,user_id):      # 设置用户基本属性，人物卡不在这里
        if user_id not in self[platform]['user_list']:
            self.add_user(U_Platform=platform,U_ID=user_id)
        self[platform][user_id][key] = value
        #if key not in self.jsonconf:
        sql_path = self.sql_path
        SQL_conn = SQL(sql_path)
        pre_sql = '''INSERT OR REPLACE INTO USER_CONF ('U_Platform','U_ID','U_Name','U_EnabledCard','U_Trust')
        VALUES(?,?,?,?,?);'''
        # pre_sql = '''INSERT OR REPLACE INTO USER_CONF ('U_Platform','U_ID','U_Name','U_EnabledCard','U_Trust','U_CriticalSuccess','U_ExtremeSuccess','U_HardSuccess','U_RegularSuccess','U_Failure','U_Fumble')
        # VALUES(?,?,?,?,?,?,?,?,?,?,?);'''
        U_Platform = self[platform][user_id]['U_Platform']
        U_Name = self[platform][user_id]['U_Name']
        U_EnabledCard = self[platform][user_id]['U_EnabledCard']
        U_Trust = self[platform][user_id]['U_Trust']
        # U_CriticalSuccess = self[platform][user_id]['U_CriticalSuccess']
        # U_ExtremeSuccess = self[platform][user_id]['U_ExtremeSuccess']
        # U_HardSuccess = self[platform][user_id]['U_HardSuccess']
        # U_RegularSuccess = self[platform][user_id]['U_RegularSuccess']
        # U_Failure = self[platform][user_id]['U_Failure']
        # U_Fumble = self[platform][user_id]['U_Fumble']
        cur = SQL_conn.connection.cursor()
        try:
            # cur.execute(pre_sql,(U_Platform,user_id,U_Name,U_EnabledCard,U_Trust,U_CriticalSuccess,U_ExtremeSuccess,U_HardSuccess,U_RegularSuccess,U_Failure,U_Fumble))
            cur.execute(pre_sql,(U_Platform,user_id,U_Name,U_EnabledCard,U_Trust))
            SQL_conn.connection.commit()
            cur.close()
            if SQL_conn.connection.total_changes == 0:
                self.log(3,'未能更改数据库数据!')
                return False
            # SQL_conn.write_sql(pre_sql,(value,key))
            return True
        except:
            self.log(4,'数据库错误，即将回滚!')
            cur.close()
            SQL_conn.connection.rollback()
            return False
        #else:

    def get_card(self,platform , user_id):
        if user_id not in self[platform]['user_list']:
            self.add_user(U_Platform=platform,U_ID=user_id)
            return {'id' : 0,'name' : '用户标准人物卡','data' : {"_null" : -1}}
        sql_conn = SQL(self.sql_path)
        en_card = self[platform][user_id]['U_EnabledCard']
        en_card_txt = 'card-'+str(en_card)
        pre_sql = '''SELECT * FROM user_{0:d}_{1:d} WHERE user_key = {2};'''.format(platform,user_id,"'"+en_card_txt+"'")
        try:
            #print('### trying to get card')
            #print(pre_sql)
            sql_conn.cursor.execute(pre_sql)#,(en_card))
            self.log(0,pre_sql)
            temp = sql_conn.cursor.fetchone()
            if temp == None:
                return {'id' : 0,'name' : '用户标准人物卡','data' : {"_null" : -1}}
            card_id_txt = temp[0][5:]
            card_id = int(card_id_txt)
            card_name = temp[1]
            card_json = temp[2]
            #print('### trying to load card')
            card_dict = json.loads(card_json)
            card = {
                'id' : card_id,
                'name' : card_name,
                'data' : card_dict
            }
            self.log(0,'loading card:'+card.__str__())
            return card
        except Exception as err:
            self.log(4,'无法读取人物卡数据！user.get_card :'+ err.__str__())
            return {'id' : 0,'name' : '用户标准人物卡','data' : {"_null" : -1}}
    def set_card(self,platform:int, user_id:int, card_dict:dict,card_name = None,en_card=-1):   # 用st进行人物卡设置
        if user_id not in self[platform]['user_list']:
            self.add_user(U_Platform=platform,U_ID=user_id)
        sql_conn = SQL(self.sql_path)
        if en_card == -1:
            en_card = self[platform][user_id]['U_EnabledCard']
        en_card_txt = 'card-'+str(en_card)
        try:
            card_json = json.dumps(card_dict)
            # 进行更新
            pre_sql = '''INSERT OR REPLACE INTO user_%d_%d VALUES (?,?,?)'''%(platform,user_id)
            sql_conn.cursor.execute(pre_sql,(en_card_txt,card_name,card_json))
            sql_conn.connection.commit()
            self.log(0,'setting card:'+en_card_txt+', '+card_name+', '+card_json)
            self.log(0,pre_sql)
            if sql_conn.connection.total_changes == 0:
                self.log(3,'未能更改数据库数据!')
                return False
            return True
        except Exception as err:
            self.log(4,'无法读取人物卡数据！user.set_card'+err.__str__())
            sql_conn.connection.rollback()
            return False
    def del_card(self,platform , user_id, card_id = None):   # 用st进行人物卡设置
        if user_id not in self[platform]['user_list']:
            self.add_user(U_Platform=platform,U_ID=user_id)
            return {}
        sql_conn = SQL(self.sql_path)
        if card_id == None:
            card_id = self[platform][user_id]['U_EnabledCard']
        card_id_txt = 'card-'+str(card_id)
        try:
            # 进行更新
            if card_id == 0:    # 如果是标准卡0，则特殊操作
                pre_sql = '''INSERT OR REPLACE INTO user_%d_%d ('user_key','val_1','val_2') VALUES ('card-0','用户标准人物卡','{"_null" : -1}')'''%(platform,user_id)
                sql_conn.cursor.execute(pre_sql)
                sql_conn.connection.commit()
                if sql_conn.connection.total_changes == 0:
                    self.log(3,'未能更改数据库数据!')
                    return False
                return True
            else:
                #pre_sql = '''INSERT OR REPLACE INTO user_%d_%d('user_key') VALUES (?)'''%(platform,user_id)
                pre_sql = '''DELETE FROM user_{0:d}_{1:d} WHERE user_key = {2};'''.format(platform,user_id,"'"+card_id_txt+"'")
                sql_conn.cursor.execute(pre_sql,card_id_txt)
                sql_conn.connection.commit()
                if sql_conn.connection.total_changes == 0:
                    self.log(3,'未能更改数据库数据!')
                    return False
                return True
        except Exception as err:
            self.log(4,'无法读取人物卡数据！user.del_card '+err.__str__())
            sql_conn.connection.rollback()
            return False
    def new_card_id(self,platform , user_id, card_name = '用户标准人物卡'):   # 用st进行人物卡设置
        if user_id not in self[platform]['user_list']:
            self.add_user(U_Platform=platform,U_ID=user_id)
            return 1
        sql_conn = SQL(self.sql_path)
        try:
            # 进行更新
            pre_sql = '''SELECT user_key FROM user_%d_%d WHERE user_key LIKE 'card-%';'''%(platform,user_id)
            sql_conn.cursor.execute(pre_sql)
            temp = sql_conn.cursor.fetchall()
            card_id_list = list()
            if temp == None:    # 如果没有人物卡则创建基本人物卡
                pre_sql = '''INSERT OR REPLACE INTO user_%d_%d VALUES (?,?,?)'''%(platform,user_id)
                sql_conn.cursor.execute(pre_sql,('card-0','用户标准人物卡','{"_null" : -1}'))
                card_id = 0
            else:
                for i in card_id_list:
                    id = int(i[0][5:])
                    card_id_list.append(id)
                card_id_list.sort()
                card_id = len(card_id_list)
                for i in range(card_id):
                    if i < card_id_list[i]:
                        card_id = i
                        break
                card_id_txt = 'card-'+str(card_id)
                pre_sql = '''INSERT OR REPLACE INTO user_%d_%d('user_key','val_1','val_2') VALUES (?,?,?)'''%(platform,user_id)
                sql_conn.cursor.execute(pre_sql,(card_id_txt,card_name,'{"_null" : -1}'))
            sql_conn.connection.commit()
            if sql_conn.connection.total_changes == 0:
                self.log(3,'未能更改数据库数据!')
                return -1
        except Exception as err:
            self.log(4,'无法读取人物卡数据！ user.new_card_id '+err.__str__())
            sql_conn.connection.rollback()
            return -1
        self.set('U_EnabledCard',card_id,platform,user_id)
        return card_id

