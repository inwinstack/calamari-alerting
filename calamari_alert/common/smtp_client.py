import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_gmail_smtp(user, password, to_account, subject, content):
    message = MIMEMultipart()
    message['From'] = user
    message['To'] = to_account
    message['Subject'] = subject
    message.attach(MIMEText(content))
    mail_server = smtplib.SMTP('smtp.gmail.com', 587)
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login(user, password)
    mail_server.sendmail(user, to_account, message.as_string())
    mail_server.close()
    return 'send successed'

send_gmail_smtp('account', 'Password', 'to_account', 'subject', 'test')
