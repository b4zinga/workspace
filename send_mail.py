# coding: utf-8
# author: myc

import smtplib
from email.header import Header
from email.mime.text import MIMEText

From = "From"
To = ['123@qq.com', ]
Subject = "Subject"


class SMTP:

    def __init__(self, host, username, password, port=465):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.smtp = smtplib.SMTP_SSL(self.host, self.port)
        self.smtp.login(self.username, self.password)

    @staticmethod
    def build_mail(content, to_address):
        mail = MIMEText(content, 'html', 'utf-8')
        mail['From'] = Header(From)
        mail['To'] = Header(to_address)
        mail['Subject'] = Header(Subject)
        return mail

    def send(self, content):
        for address in To:
            mail = self.build_mail(content, address)
            self.smtp.sendmail(self.username, address, mail.as_string())


if __name__ == '__main__':
    smtp = SMTP('smtp.qq.com', '456@qq.com', 'THIS_IS_PASSWORD')
    smtp.send('<h1>Test</h1>')
