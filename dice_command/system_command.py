# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  /
    /_/|_/_/ |_/___/_/|_/   /_/

    RainyDice 跑团投掷机器人服务 by RainyZhou
        系统控制模块 (system 指令)

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
import OlivOS
import time
from rainydice.dice_command import check_system_status,message_send

# --------------------- #
# .system xxx 功能实现  #
# --------------------- #
def getSysState(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID):
    '获取系统状态'
    # '{botname}系统状态：\n{cpu}\n{memory}\n{dick}\n{local_time}'
    replyfmt = RainyDice.GlobalVal.getGlobalMsg('getSysState')
    botname = RainyDice.bot.data['name']
    cpu = check_system_status.CpuPercent()
    memory = check_system_status.MemoryCheck()
    dick = check_system_status.DickUsage()
    localtime = check_system_status.LocalTime()
    m, s = divmod(int(time.time()-RainyDice.starttime), 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    alivetime = '{0:0>2}:{1:0>2}:{2:0>2}'.format(h,m,s)
    if d > 0:
        alivetime = str(d)+':'+alivetime
    return replyfmt.format(botname=botname,cpu=cpu,memory=memory,dick=dick,local_time=localtime,alive_time=alivetime)

def callSysRestart(plugin_event,Proc,RainyDice,message,User_ID,Group_Platform,Group_ID,msg_send):
    '远程重启框架'
    auth = RainyDice.check_user_trust(User_ID,Group_Platform)
    if auth <4:
        msg_send.attach(message_send.Msg_Reply(RainyDice.GlobalVal.getGlobalMsg('authorationFailed')))
        msg_send.send()
        return 0
    # 完成回复
    msg_reply = '即将重启 OlivOS 框架！'
    msg_send.attach(message_send.Msg_Reply(msg_reply))
    msg_send.send()
    # 框架log记录
    msg_log =  'RainyDice 远程重启框架 PLatform: {0}, User_ID: {1}, Group_ID: {2}'.format(Group_Platform,User_ID,Group_ID)
    Proc.log(2,msg_log)

    # 语句出自 /OlivOS/pluginAPI.py line 83   step_to_restart
    Proc.Proc_info.rx_queue.put(OlivOS.API.Control.packet('restart_do', Proc.Proc_name), block=False)
    return 1

