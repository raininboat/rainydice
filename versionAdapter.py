# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  /
    /_/|_/_/ |_/___/_/|_/   /_/

    RainyDice 跑团投掷机器人服务 by RainyZhou
    版本号控制实现，升级补丁

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
from rainydice import RainyDice_Version as version
import sqlite3
import json
import os

def version_updater(datapath,sqlversionFull,log):
    scriptVersion = diceversion(version)
    sqlVersion = diceversion(sqlversionFull)
    sqlpath = datapath + '/RainyDice.db'
    # 当主要版本号发生改变时不适配
    if scriptVersion.major > sqlVersion.major:
        log(5,'脚本文件版本和存档不符，无法适配！当前脚本版本：'+version+'，存档版本：'+sqlversionFull)
        return False
    # 次要版本号逻辑
    if scriptVersion.minor > sqlVersion.minor:
        log(5,'脚本文件版本和存档不符，无法适配！当前脚本版本：'+version+'，存档版本：'+sqlversionFull)
        return False
    if scriptVersion.micro > sqlVersion.micro or scriptVersion.releaseversion != sqlVersion.releaseversion:
        if sqlVersion.lessthan(0,3,5):
            # 0.3.4 => 0.3.5 版本升级
            status = __update_0_3_5(datapath)
            log(2,'完成 0.3.4 => 0.3.5 版本升级，内容：bot.json转换')
        if sqlVersion.lessthan(0,3,7):
            # 0.3.6 => 0.3.7 版本升级
            status = __update_0_3_7(datapath)
            log(2,'完成 0.3.6 => 0.3.7 版本升级，内容：重置decktmp.db')
        __sqlversionWrite(sqlpath,version)
        log(2,'当前脚本版本：'+version+'，存档版本：'+sqlversionFull+' , 已完成升级')
        return True
    log(4,'未知情况！当前脚本版本：'+version+'，存档版本：'+sqlversionFull)
    return False

class diceversion(object):
    def __init__(self,version):
        self.fullversion = version
        versionlist = str.split(version,'-')
        self.shortversion = versionlist[0]
        if len(versionlist) >=2:
            self.releaseversion = versionlist[1]
            versionlist = str.split(self.releaseversion,'.')
            self.releaselevel = versionlist[0]
            self.releaseinfo = []
            for i in range(len(versionlist)-1):
                self.releaseinfo.append(versionlist[i+1])
        versionlist = str.split(self.shortversion,'.')
        self.major = int(versionlist[0])
        self.minor = int(versionlist[1])
        self.micro = int(versionlist[2])
    def lessthan(self,major,minor,micro):
        '版本号 <= 目标值'
        if self.major>major:
            return False
        elif self.minor > minor:
            return False
        elif self.micro >= micro:
            return False
        return True

def __sqlversionWrite(sqlpath,version):
    with sqlconn(sqlpath) as conn:
        presql = '''INSERT OR REPLACE INTO basic_info ('basic_key','basic_val') VALUES (?,?);'''
        conn.execute(presql,('version',version))
        conn.commit()

class sqlconn(object):
    # sql上下文管理实现（原 try/catch 块的 with 替代）
    def __init__(self,path):
        # print('start')
        self.conn = sqlite3.connect(path)
    def __enter__(self):
        return self.conn
    def __exit__(self,exc_type, exc_val, exc_tb):
        self.conn.close()
        # return 1

def __update_0_3_5(path):
    # 0.3.4 => 0.3.5 版本升级
    # 将 bot.conf 中 tg_admin tg_master 转为 telegram_admin telegram_master
    botconfPath = path + '/conf/bot.json'
    with open(botconfPath, 'r+', encoding = 'utf-8') as file:
        botconfjson = file.read()
        file.seek(0,0)
        botconf = json.loads(botconfjson)
        botconf['telegram_admin'] = botconf['tg_admin']
        botconf['telegram_master'] = botconf['tg_master']
        del botconf['tg_admin'] , botconf['tg_master']
        botconfjson = json.dumps(botconf,ensure_ascii=False,indent='    ',sort_keys=True)
        file.write(botconfjson)
    return True

def __update_0_3_7(path):
    # 0.3.6 => 0.3.7 版本升级
    # 删除临时decktmp.db内容（内部表格存储进行重构）
    tmpdeckpath = path + '/temp/decktmp.db'
    if os.path.isfile(tmpdeckpath):
        os.remove(tmpdeckpath)
    return True
