# -*- coding: utf-8 -*-
'''
   ___  ___   _____  ____  __
  / _ \/ _ | /  _/ |/ /\ \/ /
 / , _/ __ |_/ //    /  \  / 
/_/|_/_/ |_/___/_/|_/   /_/  
                             
    外置牌堆读取至临时数据库

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

import hashlib
import sqlite3
import json
import os
import traceback

escapedict = {
    "'" : '&#39;',
    '"' : '&#34;',
    '|' : '&#124;'
}

class sqlconn(object):
    def __init__(self,path):
        # print('start')
        self.conn = sqlite3.connect(path)
    def __enter__(self):
        return self.conn
    def __exit__(self,exc_type, exc_val, exc_tb):
        if exc_type != None:
            traceback.print_exc()
        self.conn.close()

def getDeckList(publicDeckPath):
    '获取目标目录下所有json文件名称，忽略_开头项目'
    jsonlist = []
    for i in os.listdir(publicDeckPath):
        if i.endswith('.json') and not i.startswith('_'):
            jsonlist.append(i)
    return jsonlist

class DeckInfoTamplate(object):
    def __init__(self,thisfile):
        self.md5 = thisfile[0]
        self.fileName = thisfile[1]
        self.strDeckName = thisfile[2]
        self.version = thisfile[3]
        self.author = thisfile[4]
        self.doc = thisfile[5]

def getTmpSqlList(dataPath):
    tmpsqlpath = dataPath + '/temp/temp.db'
    # connTmpSql = sqlite3.connect(tmpsqlpath)
    presql = '''CREATE TABLE IF NOT EXISTS public_deck_all(
        'File_MD5'      TEXT PRIMARY KEY UNIQUE,
        'File_Name'     TEXT,
        'File_Key'      TEXT,
        'File_Version'  TEXT,
        'File_Author'   TEXT,
        'File_Doc'      TEXT
    );'''
    deckdict = {str:DeckInfoTamplate}
    
    with sqlconn(tmpsqlpath) as connTmpSql:
        cur = connTmpSql.cursor()
        cur.execute(presql)
        presql = 'SELECT * FROM public_decwk_all;'
        cur.execute(presql)
        for thisdeck in cur.fetchall():
            deckdict[thisdeck[0]] = DeckInfoTamplate(thisdeck)
        cur.close()
        connTmpSql.commit()
    # try:
    #     cur = connTmpSql.cursor()
    #     cur.execute(presql)
    #     presql = 'SELECT * FROM public_deck_all;'
    #     cur.execute(presql)
    #     for thisdeck in cur.fetchall():
    #         deckdict[thisdeck[0]] = DeckInfoTamplate(thisdeck)
    # except sqlite3.Error as err:
    #     print(err)
    # finally:
    #     cur.close()
    #     connTmpSql.commit()
    #     connTmpSql.close()
    return deckdict

def createDeckForm(dataPath,filemd5:str,filename:str,filejson:dict):
    if filejson == None:
        raise UserWarning('Json Invalid - '+filemd5)
    deckkeys = []
    tmpsqlpath = dataPath + '/temp/temp.db'
    connTmpSql = sqlite3.connect(tmpsqlpath)
    try:
        cur = connTmpSql.cursor()
        # 【创建对应牌堆表格】
        presql = '''CREATE TABLE IF NOT EXISTS deck_{filemd5}(
        'Deck_Name' text primary key,
        'Deck_CardList' text
    );'''.format(filemd5=filemd5)
        cur.execute(presql)
        presql = '''INSERT INTO deck_{filemd5}('Deck_Name','Deck_CardList') VALUES (?,?);'''.format(filemd5=filemd5)
        cardlistall = []
        for name,cardlist in filejson.items():
            if not str.startswith(name,'_'):
                deckkeys.append(name)       # _内部牌组不记录名称
            cardlistall.append((name,sqlEscape(cardlist)))
        #print(cardlistall)
        cur.executemany(presql,cardlistall)
        # 【主表中登记信息】
        presql = '''INSERT OR REPLACE INTO public_deck_all('File_MD5','File_Name','File_Key') VALUES (?,?,?);'''
        strdeckkeyall = sqlEscape(deckkeys)
        cur.execute(presql,(filemd5,filename,strdeckkeyall))
    except sqlite3.Error as err:
        print(err)
    finally:
        cur.close()
        connTmpSql.commit()
        connTmpSql.close()
    return deckkeys

def sqlEscape(datalist:list):
    '将列表内容转化为字符串用于sql存储'
    cardesclist = []
    def escape(string:str):
        string = string.replace('&','&amp;')
        for raw,esc in escapedict.items():
            string = string.replace(raw,esc)
        return string
    for thiscard in datalist:
        cardesclist.append(escape(thiscard))
    strCardAll = '|'.join(cardesclist)
    return strCardAll

def sqlUnescape(datastr:str):
    '将sql存储的字符串形式列表复原'
    cardlist = []
    def unescape(string:str):
        for raw,esc in escapedict.items():
            string = string.replace(esc,raw)
        string = string.replace('&amp;','&')
        return string
    cardtmplist = datastr.split('|')
    for cardtmp in cardtmplist:
        cardlist.append(unescape(cardtmp))
    return cardlist

def initPublicDeck(dataPath):
    '初始化，读取所有json至数据库中'
    publicDeckListAll = {}
    skipFiles = []
    publicDeckPath = dataPath + '/PublicDeck/'
    decknamelist = getDeckList(publicDeckPath)
    tmpsqllist = getTmpSqlList(dataPath)
    for filename in decknamelist:
        filehashtmp = hashlib.md5()
        with open(publicDeckPath+filename,'rb') as file:
            filebyte = file.read()
        filehashtmp.update(filebyte)
        fileMD5 = filehashtmp.hexdigest()
        if fileMD5 not in tmpsqllist.keys():
            try:
                filejson = json.loads(filebyte)
                if filejson == None:
                    print('Json Invalid - '+filename)
                    raise UserWarning('Json Invalid - '+filename)
                deckkeys = createDeckForm(dataPath,fileMD5,filename,filejson)
                for i in deckkeys:          # 本牌堆所有公共卡组全部指向对应指针
                    publicDeckListAll[i] = fileMD5
            except UserWarning:
                skipFiles.append(filename)
        else:
            thisfile = tmpsqllist[fileMD5]
            strDeckKeys = thisfile.strDeckName
            deckkeys = sqlUnescape(strDeckKeys)
            for i in deckkeys:
                publicDeckListAll[i] = fileMD5
    return publicDeckListAll,skipFiles

def getPublicDeckDict(dataPath,filemd5):
    '从数据库读取对应的牌堆'
    deckdict = {}
    tmpsqlpath = dataPath + '/temp/temp.db'
    connTmpSql = sqlite3.connect(tmpsqlpath)
    try:
        cur = connTmpSql.cursor()
        presql = '''SELECT * FROM deck_{filemd5};'''.format(filemd5=filemd5)
        cur.execute(presql)
        for name,strcardlist in cur.fetchall():
            cardlist = sqlUnescape(strcardlist)
            deckdict[name] = cardlist
    except sqlite3.Error as err:
        print(err)
    finally:
        cur.close()
        connTmpSql.close()
    return deckdict


if __name__ == '__main__':
    datapath = r'.\plugin\data\rainydice'
    print(initPublicDeck(datapath))
    # print(getPublicDeckDict(datapath,'63386cc2fc19e4ec3f7437b10ee7df18'))
