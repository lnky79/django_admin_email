# -*- coding: utf-8 -*-
"""
@file:      utils.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.5
@editor:    Vim
@create:    4/6/17 6:36 PM
@description:

"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class Email:
    """
    smtp发送邮件，对email类做一个简单的封装
    """

    def __init__(self,
                 sender,
                 receiver,
                 subject,
                 content,
                 subtype='plain',
                 img_src=None,
                 ssl=True):
        self.ssl = ssl
        self.msg = MIMEMultipart('mixed')
        msg_text = MIMEText(content, _subtype=subtype, _charset='utf-8')
        self.msg.attach(msg_text)
        if img_src:
            fp = open(img_src, 'rb')
            msg_image = MIMEImage(fp.read())
            msg_image.add_header('Content-ID', '<meinv_image.png>')
            self.msg.attach(msg_image)
            fp.close()
        self.msg['Subject'] = Header(subject, 'utf-8')
        self.msg['From'] = sender
        self.msg['To'] = receiver
        self.sender = sender
        self.receiver = receiver
        self.smtp = None

    def conn_server(self, host, port):
        # 连接服务器,并启动tls服务
        self.smtp = smtplib.SMTP(host)
        self.smtp.connect(host, port)
        if self.ssl:
            self.smtp.starttls()

    def login(self, username, password):
        self.smtp.login(username, password)
        log_string = username + '登陆成功' + '\n'
        print(log_string)
        # 可以考虑写在日志里

    def send(self):
        self.smtp.sendmail(self.sender, self.receiver, self.msg.as_string())
        log_string = '邮件已投至' + self.receiver + '\n'
        print(log_string)

    def close(self):
        self.smtp.close()
