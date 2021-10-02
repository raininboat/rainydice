# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  / 
    /_/|_/_/ |_/___/_/|_/   /_/  

    RainyDice 跑团投掷机器人服务 by RainyZhou
        所有内部常量
    
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

class __log(object):
    def __init__(self):
        self.key = ('ID','Platform','User_ID','User_Name','User_Text','Log_Time','Group_ID','Group_Name')
        self.strkey = ('User_Name','User_Text','Group_Name')
        self.colorid_str = ["#FF0000","#008000","#FFC0CB","#FFA500","#800080","#000000","#0000FF","#FFFF00","#CD5C5C","#A52A2A","#008080","#000080","#800000","#32CD32","#00FFFF","#FF00FF","#808000"]
        self.colorid_hex = [
            (0xff,0x00,0x00),(0x00,0x80,0x00),
            (0xff,0xc0,0xcb),(0xff,0xa5,0x00),
            (0x80,0x00,0x80),(0x00,0x00,0x00),
            (0x00,0x00,0xff),(0xff,0xff,0x00),
            (0xcd,0x5c,0x5c),(0xa5,0x2a,0x2a),
            (0x00,0x80,0x80),(0x00,0x00,0x80),
            (0x80,0x00,0x00),(0x32,0xcd,0x32),
            (0x00,0xff,0xff),(0xff,0x00,0xff),
            (0x80,0x80,0x00)
            ]
        self.htmlheader = '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title></title>
</head>
<body>
'''
        self.htmlend = '''\
</body>
</html>
'''


class __group(object):
    def __init__(self):
        self.key = ('Group_Platform','Group_ID','Group_Setcoc','Group_Name','Group_Owner','Group_Status','Group_Trust')
        self.singleconf = ('card','admin','name','log')
        self.statusconf = ('isBotOn','isPluginOn','isLogOn','isBanRecall')

class __user(object):
    def __init__(self):
        self.keyall = ('U_Platform','U_ID','U_Name','U_EnabledCard','U_Trust','U_CriticalSuccess','U_ExtremeSuccess','U_HardSuccess','U_RegularSuccess','U_Failure','U_Fumble')
        self.key = ('U_Platform','U_ID','U_Name','U_EnabledCard','U_Trust')
        self.card_key = ('Card_ID','Card_Name','Card_JSON')


LOG = __log()
GROUP = __group()
USER = __user()