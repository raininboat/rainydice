# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  / 
    /_/|_/_/ |_/___/_/|_/   /_/  

    RainyDice 跑团投掷机器人服务 by RainyZhou
        消息转义

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
import re as _re
from html import escape as _htmlescape , unescape as _htmlunescape 

class messageEscape(object):
    '''
    RainyDice 消息转义模块\n
    转义基于html原理，sql读取信息使用htmlunescape解除转义\n
    cqcode_replace 删除cq码中信息只保留部分类型，可用于log记录等处\n
    escape_before_save 为保存sql前转义，防止 '' 注入问题，当消息来自框架已经进行过一次转义时 & 转义可以关闭
    '''
    # cq码名称对应
    _cqcode_types = (
            ('image' , '[图片]'),
            ('record' , '[语音]'),
            ('face' , '[QQ表情]'),
            ('share' , '[链接]'),
            ('music' , '[音乐]'),
            ('reply' , '[回复]'),
            ('location' , '[位置]'),
            ('contact' , '[名片]'),
            ('anonymous' , '[匿名消息]'),
            ('redbag' , '[QQ红包]'),
            ('shake' , '[戳一戳]'),
            ('video' , '[短视频]'),
            ('forward' , '[转发消息]'),
            ('' , '[其他消息]')
    )
    htmlescape = _htmlescape
    htmlunescape = _htmlunescape
    @classmethod
    def cqcode_replace(self,text:str):
        '''
        cq码删除内容只保留类型信息，用于log等位置使用
        '''
        # at 信息单独做出来
        restr = '(\[CQ:at,qq=(\d+)\])'
        reobj = _re.findall(restr,text)
        if reobj != []:
            for cqat , qq in reobj:
                text= text.replace(cqat,'[@'+qq+']')
        restr_tamplate = '(\[CQ:{cqtype}.*?\])'
        for k,j in self._cqcode_types:
            restr = restr_tamplate.format(cqtype=k)
            reobj = _re.findall(restr,text)
            if reobj != []:
                for cqcode in reobj:
                    text= text.replace(cqcode,j)
        return text
    @classmethod
    def escape_before_save(self,string:str,amp=True):
        '''
        保存内容至sql前的转义，防止 ' " [空格] 对sql干扰\n
        & 默认转义，如果消息来自cq框架已经转义过则输入 False 不再进行操作
        '''
        if amp:
          string = string.replace('&','&amp;')  
        repldict = {
            ' ' : '&nbsp;',
            '"' : '&#34;',
            "'" : '&#39;'
            }
        for i,v in repldict.items():
            if i in string:
                string=str.replace(string,i,v)
        return string
