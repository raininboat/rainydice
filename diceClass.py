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

from rainydice import GlobalVal
from rainydice import version
# from rainydice.main import RainyDice
#from data.rainydice import *
import json
import sqlite3
class Dice(object):
    def __init__(self,Data_Path,log,cocRankCheck,ignore={}):
        self.platform_dict = {
            'qq' : 0,
            'telegram' : 1
        }
        self.sql_path = Data_Path + '/RainyDice.db'
        self.Data_path = Data_Path
        self.log = log
        self.ignore = ignore
        self.cocRankCheck = cocRankCheck
        self.bot = bot(sql_path=self.sql_path,log = log)
        self.group = Group(sql_path=self.sql_path,log = log)
        self.user = User(sql_path=self.sql_path,log = log)  # 用户信息先不读取，在开始使用时再进行读取
        self.GlobalVal = GlobalVal.GlobalVal(cocrank=cocRankCheck) 

class bot(object):
    def __init__(self,sql_path,log):
        self.log = log
        SQL_conn = SQL(sql_path)
        # 尝试新建bot_conf表
        pre_sql = '''CREATE TABLE IF NOT EXISTS BOT_CONF( 'bot_key' Text primary key NOT NULL UNIQUE ,'bot_var' text);'''
        SQL_conn.cursor.execute(pre_sql)
        pre_sql = '''SELECT * FROM BOT_CONF;'''
        SQL_conn.cursor.execute(pre_sql)
        temp = SQL_conn.cursor.fetchall()
        self.jsonconf = ['qq_admin','tg_admin']
        # print (temp)
        if temp == []:
            try:
                pre_sql = '''INSERT INTO BOT_CONF ('bot_key','bot_var') VALUES (?,?),(?,?),(?,?),(?,?),(?,?);'''
                var = ('name','本机器人','qq_master',0,'JSON','{"qq_admin":[0],"tg_admin":[0]}','tg_master',0,'version',version)
                SQL_conn.cursor.execute(pre_sql,var)
                SQL_conn.connection.commit()
                self.data = {
                    'name' : u'本机器人',
                    'version' : version,
                    'qq_master' : 0,
                    'qq_admin' : [0],
                    'tg_master': 0,
                    'tg_admin' : [0]
                }
                self.version = self.__diceversion(version)
            except:
                SQL_conn.connection.rollback()
                raise Exception('SQL ERROR','创建bot基本信息数据表失败！')
        else:
            self.data = {}
            for x in temp:
                self.data[x[0]] = x[1]
            adminJson = self.data['JSON']
            self.data['qq_admin'] = json.loads(adminJson)['qq_admin']
            self.data['tg_admin'] = json.loads(adminJson)['tg_admin']
            if 'version' not in self.data:
                self.data['version'] = '0.0.0-unknown'
            self.version = self.__diceversion(self.data['version'])
        SQL_conn.cursor.close()
        scriptversion = self.__diceversion(version)
        # 如果版本号前两位不同，则返回错误
        if self.version.major != scriptversion.major or self.version.minor != scriptversion.minor:
            log(5,'脚本文件版本和存档不符，无法适配！当前脚本版本：'+version+'，存档版本：'+self.data['version'])
            raise UserWarning('脚本文件版本和存档不符，无法适配！当前脚本版本：'+version+'，存档版本：'+self.data['version'])
        self.sql_path = sql_path
    class __diceversion(object):
        def __init__(self,version):
            self.fullversion = version
            versionlist = str.split(version,'-')
            self.shortversion = versionlist[0]
            if len(versionlist) >=2:
                releaseversion = versionlist[1]
                versionlist = str.split(releaseversion,'.')
                self.releaselevel = versionlist[0]
                self.releaseinfo = []
                for i in range(len(versionlist)-1):
                    self.releaseinfo.append(versionlist[i+1])
            versionlist = str.split(self.shortversion,'.')
            self.major = int(versionlist[0])
            self.minor = int(versionlist[1])
            self.micro = int(versionlist[2])

    def __str__(self):
        return self.fullversion   

    def set(self, key, value):      # 设置bot属性一律用这个(可以进行连接同步)，读取属性可以直接看 self.data['key'] admin等json数据除外
        self.data[key] = value  
        sql_path = self.sql_path
        SQL_conn = SQL(sql_path)
        pre_sql = '''INSERT OR REPLACE INTO BOT_CONF(bot_key,bot_var)VALUES(?,?);'''
        # '''UPDATE BOT_CONF SET bot_var = ? WHERE bot_key is ?;'''
        # '''REPLACE INTO bot_conf ('bot_key','bot_var') VALUES (?,?)'''
        # '''UPDATE bot_conf SET 'var' = 12345 WHERE 'key' is 'qq';'''
        cur = SQL_conn.connection.cursor()
        try:
            cur.execute(pre_sql,(key,value))
            SQL_conn.connection.commit()
            cur.close()
            SQL_conn.connection.total_changes
            # SQL_conn.write_sql(pre_sql,(value,key))
        except:
            raise(Exception,'sqlerror')   
    def add_admin(self,admin,platform):
        if platform == 0 :
            if admin not in self.data['qq_admin']:
                list.append(self.data['qq_admin'],admin)
        elif platform== 1:
            if admin not in self.data['tg_admin']:
                list.append(self.data['tg_admin'],admin)
        self.save_json()
    def del_admin(self,admin,platform):
        if platform == 0 :
            if admin  in self.data['qq_admin']:
                list.remove(self.data['qq_admin'],admin)
        elif platform== 1:
            if admin in self.data['tg_admin']:
                list.remove(self.data['tg_admin'],admin)
        self.save_json()
    def save_json(self):        # 将通过json存储的数据全部转化为json并保存
        tempdict = {}
        for key in self.jsonconf:
            tempdict[key] = self.data[key]
        strjson = json.dumps(tempdict)
        sql_path = self.sql_path
        SQL_conn = SQL(sql_path)
        pre_sql = '''INSERT OR REPLACE INTO BOT_CONF(bot_key,bot_var)VALUES(?,?);'''
        cur = SQL_conn.connection.cursor()
        try:
            cur.execute(pre_sql,('JSON',strjson))
            SQL_conn.connection.commit()
            cur.close()
            if SQL_conn.connection.total_changes == 0:
                self.log(3,'未能更改数据库数据!')
            # SQL_conn.write_sql(pre_sql,(value,key))
        except:
            self.log(4,'数据库错误，即将回滚!')
            SQL_conn.connection.rollback()
            cur.close()
            #raise(Exception,'sqlerror')
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
        platform_number = [0,1]         # 所有platform的数字
        # 所有键名称
        self.key = ('Group_Platform','Group_ID','Group_JSON','Group_Name','Group_Owner','Group_Status','Group_Trust')
        self.jsonconf = ['setcoc','admin']
        self.statusconf = ['isBotOn','isPluginOn','isLogOn']
        # platform 为群组出自平台，qq 为 0，tg 为 1 
        pre_sql = '''CREATE TABLE IF NOT EXISTS GROUP_CONF(
    'Group_Platform'          integer              NOT NULL,
    'Group_ID'              integer           NOT NULL,
    'Group_JSON'              TEXT            default '{"admin":[0],"setcoc":0}',
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
                s_json = self[group_temp_val[0]][group_temp_val[1]]['Group_JSON']
                tmpjson = json.loads(s_json)
                dict.update(self[group_temp_val[0]][group_temp_val[1]],tmpjson)
                b_status = self[group_temp_val[0]][group_temp_val[1]]['Group_Status']
                status = self.__bintostatus(b_status)
                dict.update(self[group_temp_val[0]][group_temp_val[1]],status)
                # self[group_temp_val[0]][group_temp_val[1]] = json.loads(s_json)
        SQL_conn.cursor.close()
        self.sql_path = sql_path
    # 将二进制存储的group_status转换为标准形式
    def __bintostatus(self,b_status):
        status = {}
        for i in range(len(self.statusconf)):
            thisbit = b_status>>i&1
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
        self[platform][group_id][key] = value
        tempdict = {}
        for tempkey in self.jsonconf:
            tempdict[tempkey] = self[platform][group_id][tempkey]
        Group_JSON = json.dumps(tempdict)
        groupdict = self[platform][group_id]
        Group_Status = self.__statustobin(groupdict)
        sql_path = self.sql_path
        SQL_conn = SQL(sql_path)
        pre_sql = '''INSERT OR REPLACE INTO GROUP_CONF ('Group_Platform','Group_ID','Group_JSON','Group_Name','Group_Owner','Group_Status','Group_Trust')
        VALUES(?,?,?,?,?,?,?);'''
        Group_Platform = self[platform][group_id]['Group_Platform']
        Group_Name = self[platform][group_id]['Group_Name']
        Group_ID = self[platform][group_id]['Group_ID']
        Group_Owner = self[platform][group_id]['Group_Owner']
        # Group_Status = self[platform][group_id]['Group_Status']
        Group_Trust = self[platform][group_id]['Group_Trust']
        try:
            SQL_conn.cursor.execute(pre_sql,(Group_Platform,Group_ID,Group_JSON,Group_Name,Group_Owner,Group_Status,Group_Trust))
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
    def add_group(self,Group_Platform,Group_ID,admin = [0],setcoc = 0,Group_Name = '群聊',Group_Owner=0,Group_Status = 3,Group_Trust = 0,isBotOn = True,isPluginOn = True,isLogOn = False):
        if Group_ID not in self[Group_Platform]['group_list']:
            self[Group_Platform]['group_list'].append(Group_ID)
        self[Group_Platform][Group_ID] = {
            'Group_Platform': Group_Platform,
            'Group_Name'    : Group_Name,
            'Group_ID'      : Group_ID,
            'Group_Owner'   : Group_Owner,
            'Group_Status'  : Group_Status,
            'Group_Trust'   : Group_Trust,
            'admin'         : admin,
            'setcoc'        : setcoc,
            'isBotOn'       : isBotOn,
            'isPluginOn'    : isPluginOn,
            'isLogOn'       : isLogOn,
        }
        tempdict = {}
        for tempkey in self.jsonconf:
            tempdict[tempkey] = self[Group_Platform][Group_ID][tempkey]
        Group_JSON = json.dumps(tempdict)
        sql_path = self.sql_path
        SQL_conn = SQL(sql_path)
        pre_sql = '''INSERT OR REPLACE INTO GROUP_CONF ('Group_Platform','Group_ID','Group_JSON','Group_Name','Group_Owner','Group_Status','Group_Trust')
        VALUES(?,?,?,?,?,?,?);'''
        
        try:
            SQL_conn.cursor.execute(pre_sql,(Group_Platform,Group_ID,Group_JSON,Group_Name,Group_Owner,Group_Status,Group_Trust))
            SQL_conn.connection.commit()
            if SQL_conn.connection.total_changes == 0:
                self.log(3,'未能更改数据库数据!')
                # SQL_conn.write_sql(pre_sql,(value,key))
                return False
            return True
        except:
            self.log(4,'数据库错误，即将回滚!')
            SQL_conn.connection.rollback()
            return False

class User(dict):
    def __init__(self,sql_path,log):
        self.log = log
        self.sql_path=sql_path
        self.platform_number = [0,1]         # 所有platform的数字
        # 所有键名称
        self.key = ('U_Platform','U_ID','U_Name','U_EnabledCard','U_Trust','U_CriticalSuccess','U_ExtremeSuccess','U_HardSuccess','U_RegularSuccess','U_Failure','U_Fumble')
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
    'U_EnabledCard'       integer         default 1,
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
        pre_sql = '''SELECT * FROM USER_CONF;'''
        SQL_conn.cursor.execute(pre_sql)
        temp = SQL_conn.cursor.fetchall()
        # print (temp)
        if not temp == []:
            for temp_val in temp:      # 单个群组
                self[temp_val[0]][temp_val[1]] = {}     # Group[平台][群号][属性]
                self[temp_val[0]]['user_list'].append(temp_val[1])
                for i in range(len(self.key)):
                    self[temp_val[0]][temp_val[1]][self.key[i]] = temp_val[i]
                # s_json = self[group_temp_val[0]][group_temp_val[1]]['Group_JSON']
                # self[group_temp_val[0]][group_temp_val[1]] = json.loads(s_json)
        SQL_conn.cursor.close()
        self.sql_path = sql_path
    # 添加新用户
    def add_user(self,U_Platform,U_ID,U_Name='用户',sender = {},U_EnabledCard=1,U_Trust=0,U_CriticalSuccess=0,U_ExtremeSuccess=0,U_HardSuccess=0,U_RegularSuccess=0,U_Failure=0,U_Fumble=0):
        # 'sender': {'age': 0, 'area': '', 'card': '', 'level': '', 'nickname': '雨鸣于舟', 'role': 'owner', 'sex': 'unknown', 'title': 'Master', 'user_id': 1620706761},
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
            'U_CriticalSuccess' : U_CriticalSuccess,
            'U_ExtremeSuccess' : U_ExtremeSuccess,
            'U_HardSuccess' : U_HardSuccess,
            'U_RegularSuccess' : U_RegularSuccess,
            'U_Failure' : U_Failure,
            'U_Fumble' : U_Fumble
        }
        # tempdict = {}
        # for tempkey in self.jsonconf:
        #     tempdict[tempkey] = self[Group_Platform][Group_ID][tempkey]
        # Group_JSON = json.dumps(tempdict)
        sql_path = self.sql_path
        SQL_conn = SQL(sql_path)
        
        try:
            #print('### trying to create tab')
            pre_sql =f''' CREATE TABLE IF NOT EXISTS user_%d_%d('Card_ID'  INTEGER PRIMARY KEY NOT NULL , 'Card_Name' text, 'Card_JSON' text);'''%(U_Platform,U_ID)
            SQL_conn.cursor.execute(pre_sql)
            #print('### trying to insert usercard')
            pre_sql =''' INSERT INTO user_%d_%d(Card_ID,Card_Name,Card_JSON) VALUES (1,'用户标准人物卡','{"_null" : -1}');'''%(U_Platform,U_ID)
            SQL_conn.cursor.execute(pre_sql)
            #print('### trying to insert user')
            pre_sql = '''INSERT OR REPLACE INTO USER_CONF ('U_Platform','U_ID','U_Name','U_EnabledCard','U_Trust','U_CriticalSuccess','U_ExtremeSuccess','U_HardSuccess','U_RegularSuccess','U_Failure','U_Fumble')
        VALUES(?,?,?,?,?,?,?,?,?,?,?);'''
            SQL_conn.cursor.execute(pre_sql,(U_Platform,U_ID,U_Name,U_EnabledCard,U_Trust,U_CriticalSuccess,U_ExtremeSuccess,U_HardSuccess,U_RegularSuccess,U_Failure,U_Fumble))
            #print('### trying to commit')
            SQL_conn.connection.commit()
            if SQL_conn.connection.total_changes == 0:
                self.log(3,'未能更改数据库数据!')
                # SQL_conn.write_sql(pre_sql,(value,key))
                return False
            return True
        except:
            self.log(4,'数据库错误，即将回滚!')
            SQL_conn.connection.rollback()
            return False
    def set(self, key, value,platform,user_id):      # 设置用户基本属性，人物卡不在这里
        if user_id not in self[platform]['user_list']:
            self.add_user(U_Platform=platform,U_ID=user_id)
        self[platform][user_id][key] = value
        #if key not in self.jsonconf:
        sql_path = self.sql_path
        SQL_conn = SQL(sql_path)
        pre_sql = '''INSERT OR REPLACE INTO USER_CONF ('U_Platform','U_ID','U_Name','U_EnabledCard','U_Trust','U_CriticalSuccess','U_ExtremeSuccess','U_HardSuccess','U_RegularSuccess','U_Failure','U_Fumble')
        VALUES(?,?,?,?,?,?,?,?,?,?,?);'''
        U_Platform = self[platform][user_id]['U_Platform']
        U_Name = self[platform][user_id]['U_Name']
        U_EnabledCard = self[platform][user_id]['U_EnabledCard']
        U_Trust = self[platform][user_id]['U_Trust']
        U_CriticalSuccess = self[platform][user_id]['U_CriticalSuccess']
        U_ExtremeSuccess = self[platform][user_id]['U_ExtremeSuccess']
        U_HardSuccess = self[platform][user_id]['U_HardSuccess']
        U_RegularSuccess = self[platform][user_id]['U_RegularSuccess']
        U_Failure = self[platform][user_id]['U_Failure']
        U_Fumble = self[platform][user_id]['U_Fumble']
        cur = SQL_conn.connection.cursor()
        try:
            cur.execute(pre_sql,(U_Platform,user_id,U_Name,U_EnabledCard,U_Trust,U_CriticalSuccess,U_ExtremeSuccess,U_HardSuccess,U_RegularSuccess,U_Failure,U_Fumble))
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
            return {'id' : 1,'name' : '用户','data' : {"_null" : -1}}
        sql_conn = SQL(self.sql_path)
        en_card = self[platform][user_id]['U_EnabledCard']
        pre_sql = '''SELECT * FROM user_%d_%d WHERE Card_ID = %d;'''%(platform,user_id,en_card)
        try:
            #print('### trying to get card')
            #print(pre_sql)
            sql_conn.cursor.execute(pre_sql)#,(en_card))
            temp = sql_conn.cursor.fetchone()
            if temp == None:
                return {'id' : 1,'name' : '用户','data' : {"_null" : -1}}
            card_id = temp[0]
            card_name = temp[1]
            card_json = temp[2]
            #print('### trying to load card')
            card_dict = json.loads(card_json)
            card = {
                'id' : card_id,
                'name' : card_name,
                'data' : card_dict
            }
            return card
        except:
            self.log(4,'无法读取人物卡数据！user.get_card')
            return {'id' : 1,'name' : '用户','data' : {"_null" : -1}}
    def set_card(self,platform , user_id, card_dict ,card_name = None,en_card=-1):   # 用st进行人物卡设置
        if user_id not in self[platform]['user_list']:
            self.add_user(U_Platform=platform,U_ID=user_id)
        sql_conn = SQL(self.sql_path)
        if en_card == -1:
            en_card = self[platform][user_id]['U_EnabledCard']
        pre_sql = '''SELECT * FROM user_%d_%d WHERE Card_ID = %d;'''%(platform,user_id,en_card)
        try:
            #print(pre_sql)
            sql_conn.cursor.execute(pre_sql)
            temp = sql_conn.cursor.fetchone()
            if temp == None:
                temp = [1,'用户','{"_null" : -1}']
            card_id = temp[0]
            #print(temp)
            if card_name == None:
                card_name = temp[1]
            card_json = temp[2]
            card_dict_all = json.loads(card_json)
            dict.update(card_dict_all,card_dict)        # 用新字典覆盖原有技能值
            card_json = json.dumps(card_dict)
            # 进行更新
            pre_sql = '''INSERT OR REPLACE INTO user_%d_%d VALUES (?,?,?)'''%(platform,user_id)
            sql_conn.cursor.execute(pre_sql,(en_card,card_name,card_json))
            sql_conn.connection.commit()
            if sql_conn.connection.total_changes == 0:
                self.log(3,'未能更改数据库数据!')
                return False
            return True
        except:
            self.log(4,'无法读取人物卡数据！user.set_card')
            sql_conn.connection.rollback()
            return False
    def del_card(self,platform , user_id, card_id = None):   # 用st进行人物卡设置
        if user_id not in self[platform]['user_list']:
            self.add_user(U_Platform=platform,U_ID=user_id)
            return {}
        sql_conn = SQL(self.sql_path)
        if card_id == None:
            card_id = self[platform][user_id]['U_EnabledCard']
        try:
            # 进行更新
            if card_id == 1:    # 如果是标准卡1，则特殊操作
                pre_sql = '''INSERT OR REPLACE INTO user_%d_%d (Card_ID,Card_Name,Card_JSON) VALUES (1,'用户标准人物卡','{"_null" : -1}')'''%(platform,user_id)
                sql_conn.cursor.execute(pre_sql)
                sql_conn.connection.commit()
                if sql_conn.connection.total_changes == 0:
                    self.log(3,'未能更改数据库数据!')
                    return False
                return True
            else:
                pre_sql = '''INSERT OR REPLACE INTO user_%d_%d(Card_ID) VALUES (?)'''%(platform,user_id)
                sql_conn.cursor.execute(pre_sql,(card_id))
                sql_conn.connection.commit()
                if sql_conn.connection.total_changes == 0:
                    self.log(3,'未能更改数据库数据!')
                    return False
                return True
        except:
            self.log(4,'无法读取人物卡数据！user.del_card')
            sql_conn.connection.rollback()
            return False
    def new_card_id(self,platform , user_id, card_name = '用户'):   # 用st进行人物卡设置
        if user_id not in self[platform]['user_list']:
            self.add_user(U_Platform=platform,U_ID=user_id)
            return 1
        sql_conn = SQL(self.sql_path)
        try:
            # 进行更新
            pre_sql = '''SELECT Card_ID FROM user_%d_%d WHERE Card_Name IS NULL ORDER BY Card_ID ASC'''%(platform,user_id)
            sql_conn.cursor.execute(pre_sql)
            temp = sql_conn.cursor.fetchone()
            if temp == None:
                pre_sql = '''INSERT INTO user_%d_%d('Card_Name') VALUES (?)'''%(platform,user_id)
                sql_conn.cursor.execute(pre_sql,(card_name))
                pre_sql = '''SELECT Card_ID FROM user_%d_%d ORDER BY Card_ID DESC'''%(platform,user_id)
                sql_conn.cursor.execute(pre_sql)
                temp = sql_conn.cursor.fetchone()
                card_id = temp[0]
            else:
                card_id = temp[0]
                pre_sql = '''INSERT INTO user_%d_%d(Card_ID,Card_Name) VALUES (?,?)'''%(platform,user_id)
                sql_conn.cursor.execute(pre_sql,(card_id,card_name))
            sql_conn.connection.commit()
            if sql_conn.connection.total_changes == 0:
                self.log(3,'未能更改数据库数据!')
                return -1
        except:
            self.log(4,'无法读取人物卡数据！ user.new_card_id')
            sql_conn.connection.rollback()
            return -1
        self.set('U_EnabledCard',card_id,platform,user_id)
        return card_id
    