# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  / 
    /_/|_/_/ |_/___/_/|_/   /_/  

    RainyDice 跑团投掷机器人服务 by RainyZhou
        骰娘模块化实现

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
# 这里的都是对外的真正指令接口模块
# 内部实现模块的导入通过脚本内 from rainydice.dice_command import xxx 实现

# .system 指令模块
from rainydice.dice_command import system_command
# .log 模块 & log 内部记录和渲染接口 
from rainydice.dice_command import chat_log
# .ra 指令重构
from rainydice.dice_command import ra_command
# .jrrp 今日人品
from rainydice.dice_command import jrrp_command
# .draw 抽卡模块
from rainydice.dice_command import draw_command
# .coc 人物卡做成
from rainydice.dice_command import coc_card_new