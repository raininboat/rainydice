# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  / 
    /_/|_/_/ |_/___/_/|_/   /_/  

    RainyDice 跑团投掷机器人服务 by RainyZhou
    版本号控制实现

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
from rainydice import version
import sqlite3

def version_updater(sqlpath,sqlversionFull):
    scriptVersionFull = version
    scriptVersion = diceversion(version)
    sqlVersion = diceversion(sqlversionFull)
    sqlpath = sqlpath
    # 当主要版本号发生改变时不适配
    if scriptVersion.major > sqlVersion.major:
        return False,(5,'脚本文件版本和存档不符，无法适配！当前脚本版本：'+version+'，存档版本：'+sqlversionFull)
    # 次要版本号逻辑
    if scriptVersion.minor > sqlVersion.minor:
        return False,(5,'脚本文件版本和存档不符，无法适配！当前脚本版本：'+version+'，存档版本：'+sqlversionFull)
    if scriptVersion.micro > sqlVersion.micro or scriptVersion.releaseversion != sqlVersion.releaseversion:
        __sqlversionWrite(sqlpath,version)
        return True,(2,'当前脚本版本：'+version+'，存档版本：'+sqlversionFull+' , 自动完成升级')
    return False , (4,'未知情况！当前脚本版本：'+version+'，存档版本：'+sqlversionFull)    
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

def __sqlversionWrite(sqlpath,version):
    conn = __SQL(sqlpath)
    presql = '''INSERT OR REPLACE INTO basic_info ('basic_key','basic_val') VALUES (?,?);'''
    conn.cursor.execute(presql,('version',version))    
    conn.connection.commit()

class __SQL(object):
    def __init__(self,Path):
        self.connection = sqlite3.connect(Path)
        self.cursor = self.connection.cursor()
        self.path = Path
    def __del__(self):
        self.cursor.close()
        self.connection.close()