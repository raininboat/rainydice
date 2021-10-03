# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  / 
    /_/|_/_/ |_/___/_/|_/   /_/  

    RainyDice 跑团投掷机器人服务 by RainyZhou
        系统状态监控（psutil转接口）
    
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
# 查看系统使用情况的专用模块，OlivOS框架已经使用无需再次强调需要安装
# psutil官方文档位置 <https://psutil.readthedocs.io/en/latest/>
from time import time
import psutil
from datetime import datetime

# ---------------------- #
# PSUTIL 模块本地转接口等 #
# ---------------------- #

def LocalTime(formattime:str or None=None):
    '''
    查看本地时间，formattime 为本地时间格式化方式

    local time: %Y-%m-%d %H:%M:%S
    '''
    if formattime == None:
        formattime = "local time: %Y-%m-%d %H:%M:%S"
    return  datetime.fromtimestamp(time()).strftime(formattime)

def MemoryCheck():
    '''
    查看当前系统内存使用情况,可直接__str__()输出字符串结果
    
    Memory: {used}GB / {total}GB => {percent}%
    '''
    return __MemoryCheck()

def DickUsage(path:str or None=None):
    '''
    查看当前磁盘使用情况,path填写后可选择不同磁盘,可直接__str__()输出字符串结果
    
    Dick Usage: {used}GB / {total}GB => {percent}%
    '''
    if path == None:
        path = '/'
    return __DickUsage(path)

def BootTime(timestamp:bool=False,formattime:str=None):
    '''
    获取系统启动时间，timestamp 为 True 时直接返回timestamp 
    否则返回时间字符串（可用format自定义）

    %Y-%m-%d %H:%M:%S
    '''
    if timestamp:
        return psutil.boot_time()
    else:
        if formattime == None:
            formattime = "%Y-%m-%d %H:%M:%S"
        return datetime.fromtimestamp(psutil.boot_time()).strftime(formattime)

def CpuPercent(interval=None):
    '''
    对cpu使用率的转接口，interval 填写非负数后阻塞读取cpu使用情况，
    为 None 则返回自上次使用后的结果（第一次恒为0）
    '''
    return __CpuPercent(interval=interval)

# ------------ #
# 内部 api 实现 #
# ------------ #

class __CpuPercent(object):
    def __init__(self,interval):
        self.percent = psutil.cpu_percent(interval=interval)
    def __str__(self,formatstr:str or None =None):
        if formatstr==None:
            formatstr = 'CPU: {percent}%'
        return formatstr.format(percent=self.percent)
class __MemoryCheck(object):
    def __init__(self):
        mem = psutil.virtual_memory()
        self.total = round(float(mem.total / 1024 / 1024 /1024),2)
        self.available = round(float(mem.available / 1024 / 1024 /1024),2)
        self.used = round(self.total - self.available,2)
        self.percent = round(100 * self.used / self.total,1)
        # print(usedMem.__str__()+' / '+totalMem.__str__()+' GB')
        # return (self.usedMem,self.totalMem)
    def __str__(self,formatstr:str or None=None):
        if formatstr == None:
            formatstr = 'Memory: {used}GB / {total}GB => {percent}%'
        # reply = formatstr.format(usedMem=self.usedMem,totalMem=self.totalMem,percent=self.percent)
        return formatstr.format(used=self.used,total=self.total,percent=self.percent)

class __DickUsage(object):
    def __init__(self,path):
        dickState = psutil.disk_usage(path)
        self.total = round(float(dickState.total / 1024 / 1024 /1024),2)
        self.used = round(float(dickState.used / 1024 / 1024 /1024),2)
        self.percent = dickState.percent
        # print(usedMem.__str__()+' / '+totalMem.__str__()+' GB')
        # return (self.usedMem,self.totalMem)
    def __str__(self,formatstr:str or None=None):
        if formatstr == None:
            formatstr = 'Dick Usage: {used}GB / {total}GB => {percent}%'
        # reply = formatstr.format(usedMem=self.usedMem,totalMem=self.totalMem,percent=self.percent)
        return formatstr.format(used=self.used,total=self.total,percent=self.percent)

# if __name__ == '__main__':
#     print(CpuPercent(interval=1))
#     print(BootTime())
#     print(MemoryCheck())
#     print(DickUsage().__str__())
