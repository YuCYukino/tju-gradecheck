'''
/************************************************************************
*
*   
*    File Name: 天津大学成绩/通知（半）自动查询
*    Description: 根据网上大佬们的代码,利用helium,简单撰写了一个半自动查询脚本，单查个成绩或者通知
还是很简单的
*
*    Version: V1.0
*    Author: yukino
*    Create Time: 2022-09-21
*
*************************************************************************/

'''
#引入selenium库中的 webdriver 模块
from genericpath import exists
from multiprocessing.connection import wait
from os import kill
from helium import *
import time
from sendemail import buildtext, emailsend, smtplib
import smtplib
from email.mime.text import MIMEText
from email.header import Header

#设置邮箱，自行百度如何开通SMTP服务，以QQ邮箱为例，别的邮箱改一下host_name
host_name = 'smtp.qq.com'
username = 'example@qq.com'
token = ' ' #开通SMTP后会有个密码，填进来即可

#查成绩用
driver = start_chrome('http://classes.tju.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR')
wait_until(Text("平均绩点").exists,60,3)

'''
#查通知用
driver = start_chrome('http://ee.tju.edu.cn/News/noticeList.do')
wait_until(Text("通知通告").exists,60,3)
'''

#自己定义想查什么，填在下面双引号即可，48行同理
a=Text(" ").exists()

while(not a):
    #可以自己定义时间，建议不要太短
    time.sleep(180.0)
    a=Text(" ").exists()
    refresh()
#查到了，退出循环，发邮件
emailsend(buildtext(),username)
kill_browser()

'''
下面这些代码来源网络，自己只做了一点修改
'''

def emailsend(body, receiver, host=host_name, user=username, email_token=token):
    # 第三方 SMTP 服务
    mail_host = host  
    mail_user = user  
    mail_pass = email_token  

    sender = mail_user
    receivers = [receiver]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(body, 'plain', 'utf-8')

    #邮件题目，想起什么都行，例如下面
    message['From'] = Header("天津大学分数更新提示系统")
    #message['From'] = Header("天津大学新通知发布提示系统")

    message['To'] = Header('您' + receivers[0])

    #邮件主题，同理，自己起名也行
    subject = '您有新的成绩更新!'
    #subject = '国庆节放假通知来啦'

    message['Subject'] = Header(subject, 'utf-8')

    try:
        server = smtplib.SMTP(mail_host, 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        print('[{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), end='')
        print('正在登录smtp发信服务器...')
        server.login(mail_user, mail_pass)
        text = message.as_string()
        server.sendmail(sender, receivers, text)
        server.close()
        print('[{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), end='')
        print('邮件发送成功!')
    except:
        if mail_user == "" or mail_pass == '':
            print('[{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), end='')
            print('邮件发送失败,原因是没有填写第三方SMTP服务器的用户名和口令,请在emailsend.py文件中填写好!')
            print('[{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), end='')
            print('程序将在10秒钟后自动退出!')
            time.sleep(10)
            exit()
        print('[{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), end='')
        print('邮件发送失败!(发生了未知的错误)')


def buildtext():
    #邮件内容，可以自己定义
    textbody = "才考这点分？"
    return textbody
