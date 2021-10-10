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
import shutil
import sys
import traceback

escapedict = {
    "'" : '&#39;',
    '"' : '&#34;',
    '|' : '&#124;'
}

class sqlconn(object):
    # sql上下文管理实现（原 try/catch 块的 with 替代）
    def __init__(self,path):
        # print('start')
        self.conn = sqlite3.connect(path)
    def __enter__(self):
        return self.conn
    def __exit__(self,exc_type, exc_val, exc_tb):
        if exc_type != None:
            traceback.print_exc()
        self.conn.close()
        # return 1

def getDeckList(publicDeckPath):
    '获取目标目录下所有json文件名称，忽略_开头项目'
    jsonlist = []
    for i in os.listdir(publicDeckPath):
        if i.endswith('.json') and not i.startswith('_'):
            jsonlist.append(i)
    return jsonlist

class DeckInfoTamplate(object):
    def __init__(self,thisfile):
        if type(thisfile) == list or type(thisfile) == tuple:
            self.md5 = thisfile[0]
            self.fileName = thisfile[1]
            self.strDeckName = thisfile[2]
            self.title = thisfile[3]
            self.namespace = thisfile[4]
            self.dependence = sqlUnescape(thisfile[5])
            self.version = thisfile[6]
            self.author = thisfile[7]
            self.doc = thisfile[8]
        elif type(thisfile) == dict:
            self.md5 = thisfile['file_md5']
            self.fileName = thisfile['file_name']
            self.strDeckName = thisfile['file_key']
            self.title = thisfile['file_title']
            self.namespace = thisfile['file_namespace']
            self.dependence = sqlUnescape(thisfile['str_file_dependence'])
            self.version = thisfile['file_version']
            self.author = thisfile['file_author']
            self.doc = thisfile['file_doc']
    def __str__(self):
        string = '<DeckInfoTamplate: md5={0}, fileName={1}, strDeckDame={2}, title={3}, namespace={4}, dependence={5}, version={6}, author={7}, doc={8} >'
        return string.format(self.md5,self.fileName,self.strDeckName,self.title,self.namespace,self.dependence.__str__(),self.version,self.author,self.doc)

def getTmpSqlList(dataPath):
    tmpsqlpath = dataPath + '/temp/decktmp.db'
    # connTmpSql = sqlite3.connect(tmpsqlpath)
    presql = '''CREATE TABLE IF NOT EXISTS public_deck_all(
        'File_MD5'      TEXT PRIMARY KEY UNIQUE,
        'File_Name'     TEXT,
        'File_Key'      TEXT,
        'File_Title'    TEXT,
        'File_Namespace' TEXT,
        'File_Dependence' TEXT,
        'File_Version'  TEXT,
        'File_Author'   TEXT,
        'File_Doc'      TEXT
    );'''
    deckdict = {str:DeckInfoTamplate}
    with sqlconn(tmpsqlpath) as connTmpSql:
        cur = connTmpSql.cursor()
        cur.execute(presql)
        presql = 'SELECT * FROM public_deck_all;'
        cur.execute(presql)
        for thisdeck in cur.fetchall():
            deckdict[thisdeck[0]] = DeckInfoTamplate(thisdeck)
        cur.close()
        connTmpSql.commit()
    return deckdict

def createDeckForm(dataPath,filemd5:str,filename:str,filejson:dict):
    if filejson == None:
        raise UserWarning('Json Invalid - '+filemd5)
    deckkeys = []
    fileMetaInfo = {
        'file_md5' : filemd5,
        'file_name' : filename,
        'file_key' : '',
        'file_title' : filemd5,
        'file_namespace' : filemd5,
        'str_file_dependence' : '',
        'file_version' : 'unknown',
        'file_author' : 'unknown',
        'file_doc' : 'unknown'
    }
    tmpsqlpath = dataPath + '/temp/decktmp.db'
    with sqlconn(tmpsqlpath) as connTmpSql:
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
            if str.startswith(name,'$'):    # 牌堆元信息，
                if name == '$title':
                    fileMetaInfo['file_title'] = cardlist
                elif name == '$namespace':
                    fileMetaInfo['file_namespace'] = cardlist
                elif name == '$dependence':
                    fileMetaInfo['str_file_dependence'] = sqlEscape(cardlist)
                elif name == '$author':
                    fileMetaInfo['file_author'] = cardlist
                elif name == '$version':
                    fileMetaInfo['file_version'] = cardlist
                elif name == '$doc':
                    fileMetaInfo['file_doc'] = cardlist
                continue
            if not str.startswith(name,'_'):
                deckkeys.append(name)       # _内部牌组不记录名称
            cardlistall.append((name,sqlEscape(cardlist)))
        #print(cardlistall)
        cur.executemany(presql,cardlistall)
        # 【主表中登记信息】
        presql = '''INSERT OR REPLACE INTO public_deck_all('File_MD5','File_Name','File_Key','File_Title','File_Namespace','File_Dependence','File_Version','File_Author','File_Doc') 
        VALUES (:file_md5,:file_name,:file_key,:file_title,:file_namespace,:str_file_dependence,:file_version,:file_author,:file_doc);'''
        fileMetaInfo['file_key'] = sqlEscape(deckkeys)
        # strdeckkeyall = sqlEscape(deckkeys)
        cur.execute(presql,fileMetaInfo)
        cur.close()
        connTmpSql.commit()
    return deckkeys,DeckInfoTamplate(fileMetaInfo)

def sqlEscape(datalist:list):
    '将列表内容转化为字符串用于sql存储'
    if datalist == [] :
        return ''
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
    if datastr == '' :
        return []
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
    publicDeckListAll = {}      # 所有文件中的卡组，可抽卡堆(str) -> 文件md5(str)（临时数据库读取）
    fileMetaInfoAll = {}              # 各牌堆文件的信息 文件md5(str) -> (DeckInfoTamplate)
    skipFiles = []              # 读取失败忽略的文件
    publicDeckPath = dataPath + '/PublicDeck/'
    decknamelist = getDeckList(publicDeckPath)
    if 'default.json' not in decknamelist:
        # 如果默认牌堆不存在则复制进入 PublicDeck
        scriptPath = sys.path[0]
        shutil.copy(scriptPath+'/plugin/app/rainydice/src/default.json',publicDeckPath)
        decknamelist.append('default.json')
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
                deckkeys,metainfo = createDeckForm(dataPath,fileMD5,filename,filejson)
                for i in deckkeys:          # 本牌堆所有公共卡组全部指向对应指针
                    publicDeckListAll[i] = fileMD5
                fileMetaInfoAll[fileMD5] = metainfo
                    
            except Exception as err:
                print(traceback.print_exc())
                skipFiles.append(filename)
        else:
            thisfile = tmpsqllist[fileMD5]
            fileMetaInfoAll[fileMD5] = thisfile
            strDeckKeys = thisfile.strDeckName
            deckkeys = sqlUnescape(strDeckKeys)
            for i in deckkeys:
                publicDeckListAll[i] = fileMD5
    return publicDeckListAll,skipFiles,fileMetaInfoAll

def getPublicDeckDict(dataPath,filemd5):
    '从数据库读取对应的牌堆'
    deckdict = {}
    tmpsqlpath = dataPath + '/temp/decktmp.db'
    with sqlconn(tmpsqlpath) as connTmpSql:
        cur = connTmpSql.cursor()
        presql = '''SELECT * FROM deck_{filemd5};'''.format(filemd5=filemd5)
        cur.execute(presql)
        for name,strcardlist in cur.fetchall():
            cardlist = sqlUnescape(strcardlist)
            deckdict[name] = cardlist
    return deckdict

def loadDeck(dataPath,fileMetaInfoDict:DeckInfoTamplate):
    dependence = fileMetaInfoDict.dependence
    deckdict = getPublicDeckDict(dataPath,fileMetaInfoDict.md5)
    if dependence == []:
        return deckdict
    loaddeckmd5list = []
    tmpsqlpath = dataPath + '/temp/decktmp.db'
    with sqlconn(tmpsqlpath) as connTmpSql:
        cur = connTmpSql.cursor()
        for title in dependence:        
            presql = '''SELECT File_MD5 FROM public_deck_all WHERE File_Namespace = ? '''
            cur.execute(presql,(title,))
            res = cur.fetchall()
            for i in res:
                if i[0] not in loaddeckmd5list:
                    loaddeckmd5list.append(i[0])
    for filemd5 in loaddeckmd5list:
        deckdict.update(getPublicDeckDict(dataPath,filemd5))
    return deckdict

# if __name__ == '__main__':
#     datapath = r'.\plugin\data\rainydice'
#     a = initPublicDeck(datapath)
#     # print(a[0])
#     #print(getPublicDeckDict(datapath,'63386cc2fc19e4ec3f7437b10ee7df18'))
#     print(gerDependenceDict(datapath,a[2][a[0]['大成功']]))
