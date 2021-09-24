import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
# import threading 还是不去搞成多线程了

# 转换收件人信息
def __formatrawaddr(receiver_raw:list):
    string = ''
    receiver = []
    for i in receiver_raw:
        string = string + formataddr(i,'utf-8') + ','
        receiver.append(i[1])
    return string[:-1],receiver
# 添加附件
def __att(path,filename,encoding='utf-8'):
    with open(path+filename,'r',encoding=encoding) as file:
        att1 = MIMEText(file.read(), 'base64', encoding)
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="{0}"'.format(filename)
    return att1
def send_email(botconf:dict,logpath:str,receiver_raw:list):
    message = MIMEMultipart()
    useraddr = botconf['email']['useraddr']
    message['From'] = formataddr((botconf['name'],useraddr),'utf-8')
    message['To'],receivers = __formatrawaddr(receiver_raw)
    message['Subject'] = Header('跑团记录获取', 'utf-8')
    with open(logpath+'log.html','r',encoding='utf-8') as file:
        message.attach(MIMEText(file.read(), 'html', 'utf-8'))
    if botconf['log']['txtRaw']:
        att1 = __att(logpath,'log_raw.txt','utf-8')
        message.attach(att1)
    if botconf['log']['csv']:
        att2 = __att(logpath,'log_form.csv','utf-8-sig')
        message.attach(att2)
    if botconf['log']['doc']:
        pass
    host = botconf['email']['host']
    port = botconf['email']['port']
    password = botconf['email']['password']
    try:
        if botconf['email']['ssl']:
            mail = smtplib.SMTP_SSL(host=host,port=port)
        else:
            mail = smtplib.SMTP(host=host,port=port)
        a = mail.login(user=useraddr,password=password)
        # print(a)
        # print(useraddr)
        # print(receivers)
        # print(message.as_string())
        mail.sendmail(from_addr=useraddr,to_addrs=receivers,msg=message.as_string())
        status = True
    except smtplib.SMTPException as err:
        status = False
        try:
            errtxt = err.args[1].decode('gbk')
            print(str(err.args[0])+errtxt)
        except Exception:
            print(str(err.args[0]))
    finally:
        mail.close()
    return status
