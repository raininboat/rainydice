# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  /
    /_/|_/_/ |_/___/_/|_/   /_/

    RainyDice 跑团投掷机器人服务 by RainyZhou
        全局变量

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

class GlobalVal(object):
    def __init__(self,cocrank:dict):
        self.GlobalVal['setcocExplain']=[None]*len(cocrank)
        for i,v in cocrank.items():
            self.GlobalVal['setcocExplain'][i]=v['text']
    def getHelpDoc(self,key='') : # 最大子串不会先不做了，现在只是自动把&关联项转换完毕
        if key in self.HelpDoc:
            temp = self.HelpDoc[key]
            if temp[0] == '&':
                newKey = temp[1:]
                temp = self.getHelpDoc(key=newKey)
            return temp
        else:
            return 'Help Doc: '+key

    def getGlobalMsg(self,key=''):
        if key in self.GlobalMsg:
            temp = self.GlobalMsg[key]
            if temp[0] == '&':
                newKey = temp[1:]
                temp = self.getGlobalMsg(key=newKey)
            return temp
        else:
            return ''
    # 所有指令开始符号（只有这些会匹配）
    Command_Start_Sign = ('.','。','/')
    GlobalMsg = {
        'BotMsg' : 'RainyDice by Rainy Zhou\n测试版 V{version}',
        'BotOnReply' : '已成功开启{bot_name}',
        'BotOffReply' : '已成功关闭{bot_name}',
        'InputErr' : '请认真核对输入的内容！',
        'GroupCmdErr':'{Command_Name}只能在群聊中使用',
        'SkillUnsetErr' : '{Skill_Name}技能值未设定！\n请先使用 .st 进行设定',
        'rdReply' : '{User_Name}进行投掷:\n{DiceExp}={DiceStep}{Result}',
        'raReply' : '{reason}{User_Name}进行{Skill_Name}检定:\n{sign}={step}={result} / {Skill_Val} {rank}',
        'rhGroupReply' : '{User_Name}进行了一次暗骰',
        'rhPrivateReply' : '在[{Group_Name}]({Group_ID})中,{User_Name}进行投掷:\n{DiceExp}={DiceStep}{Result}',
        'scReply' : '{User_Name}进行理智检定:\nD100 = {Roll_Result} / {Old_San} {Rank}\n理智损失: {San_Lose_Expression} = {San_Lose_Result} \n当前理智：{nowSan}',
        'scSanNull' : '理智值未输入或无效，请使用.st将其设置为正整数',
        'stDelReply' : '已将{Card_Name}的属性【{Skill_Name}】删除',
        'stClrReply' : '已将{Card_Name}的属性全部清除',
        'stSetReply' : '属性设定成功',
        'stShowAllReply' : '{User_Name}的人物卡[{Card_ID}]({Card_Name})属性为：\n',
        'stNameReply' : '已将{User_Name}的人物卡[{Card_ID}]({Card_Name})名称改为：{New_Name}',
        'stShowReply' : '{User_Name}的人物卡[{Card_ID}]({Card_Name})中属性【{Skill_Name}】为：{Skill_Val}',
        'stChangeReply' : '已记录{User_Name}的属性变化:\n{Skill_Name}：{Skill_Val}{Change_Expression} = {Skill_Val}{Change_Result} = {Skill_Val_Result}',
        'stNewCardReply' : '已记录{User_Name}的人物卡S\n[{Card_ID}]({Card_Name})',
        'enReplyFail' : '{User_Name}进行 {Skill_Name} 幕间成长:\nD100 = {Roll} / {Old_Skill} 失败！',
        'enReplySuccess' : '{User_Name}进行 {Skill_Name} 幕间成长:\nD100 = {Roll} / {Old_Skill} 成功！\n{Skill_Name}：{Old_Skill}+{En_Exp}={Old_Skill}+{En_Step}={Now_Skill}',
        'nnReply' : '已将{User_Name}的用户名称改为：{New_Name}',
        'OnlyInGroup' : '该指令只能在群聊中使用！',
        'setcocReply' : '群聊房规属性已改为{setcoc}:\n{setcocExplain}',
        'logAlreadyOn' : '当前log已开启',
        'logAlreadyOff' : '当前log已经关闭',
        'logOnReply' : 'log记录开启！请使用.log off 暂停 或 .log end 结束并发送log至邮箱',
        'logOffReply' : 'log已关闭',
        'logEndReply' : 'log完成，正在生成文件并发送',
        'authorationFailed' : '你没有本权限！',
        'getSysState' : '{botname}系统状态：\n{cpu}\n{memory}\n{dick}\n{local_time}\n插件已启动时间: {alive_time}',
        'strJrrpReply' : '{username}的今日人品值: {jrrp}',
        'strDrawReply' : '{username}的进行抽卡: \n{card}'
    }
    GlobalVal = {
        'rankName' : ["【未知情况】","大成功","极难成功","困难成功","成功","失败","大失败"],
        'setcocExplain' : []     # 请修改randcheck进行自定义

    }
    HelpDoc = {
        'ra' : 'ra/rc帮助信息',
        'rc' : '&ra',
        'sc' : 'sc帮助信息',
        'nn' : 'nn帮助信息',
        'rd' : 'rd帮助信息'
    }