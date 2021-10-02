# -*- coding: utf-8 -*-
'''
       ___  ___   _____  ____  __
      / _ \/ _ | /  _/ |/ /\ \/ /
     / , _/ __ |_/ //    /  \  / 
    /_/|_/_/ |_/___/_/|_/   /_/  

    RainyDice 跑团投掷机器人服务 by RainyZhou
        log 邮件发送模块

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
import smtplib as __smtplib
from email.header import Header as __Header
from email.mime.multipart import MIMEMultipart as __MIMEMultipart
from email.mime.text import MIMEText as __MIMEText
from email.mime.base import MIMEBase as __MIMEBase
from email.utils import formataddr as __formataddr
from email.encoders import encode_base64 as __encode_base64
# import threading 还是不去搞成多线程了

# 转换收件人信息
def __formatrawaddr(receiver_raw:list):
    string = ''
    receiver = []
    for i in receiver_raw:
        string = string + __formataddr(i,'utf-8') + ','
        receiver.append(i[1])
    return string[:-1],receiver
# 添加附件
def __att(path,filename,encoding='utf-8'): 
    with open(path+filename,'r',encoding=encoding) as file:
        att1 = __MIMEText(file.read(), 'base64', encoding)
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="{0}"'.format(filename)
    return att1
def __att2(path,filename):
    file_msg = __MIMEBase('application', 'octet-stream')  
    with open(path+filename,mode='rb') as file:
        file_msg.set_payload(file.read())
    __encode_base64(file_msg)
    file_msg.add_header('Content-Disposition','attachment', filename = filename)
    return file_msg

def send_email(botconf:dict,logpath:str,receiver_raw:list):
    message = __MIMEMultipart()
    useraddr = botconf['email']['useraddr']
    message['From'] = __formataddr((botconf['name'],useraddr),'utf-8')
    message['To'],receivers = __formatrawaddr(receiver_raw)
    message['Subject'] = __Header('跑团记录获取', 'utf-8')
    if botconf['log']['html']:
        with open(logpath+'log.html','r',encoding='utf-8') as file:
            message.attach(__MIMEText(file.read(), 'html', 'utf-8'))
    else:
        message.attach(__MIMEText('Rainy Dice 跑团记录获取，请在附件中下载 log文件', 'plain', 'utf-8'))
    if botconf['log']['txtRaw']:
        att1 = __att(logpath,'raw.txt','utf-8')
        message.attach(att1)
    if botconf['log']['csv']:
        att2 = __att(logpath,'log_form.csv','utf-8-sig')
        message.attach(att2)
    if botconf['log']['doc']:
        att3 = __att2(logpath,'log.docx')
        message.attach(att3)
    host = botconf['email']['host']
    port = botconf['email']['port']
    password = botconf['email']['password']
    try:
        if botconf['email']['ssl']:
            mail = __smtplib.SMTP_SSL(host=host,port=port)
        else:
            mail = __smtplib.SMTP(host=host,port=port)
        a = mail.login(user=useraddr,password=password)
        # print(a)
        # print(useraddr)
        # print(receivers)
        # print(message.as_string())
        mail.sendmail(from_addr=useraddr,to_addrs=receivers,msg=message.as_string())
        status = True
    except __smtplib.SMTPException as err:
        status = False
        try:
            errtxt = err.args[1].decode('gbk')
            print(str(err.args[0])+errtxt)
        except Exception:
            print(str(err.args[0]))
    finally:
        mail.close()
    return status
