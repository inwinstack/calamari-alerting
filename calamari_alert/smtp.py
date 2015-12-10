import smtplib
from common import logs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SMTPClient(object):

    def __init__(self, user, password, domain_name, port):
        self.user = user
        self.password = password
        self.domain_name = domain_name
        self.port = port

    def sent(self, to_account, content):
        message = MIMEMultipart()
        message['From'] = self.user
        message['To'] = to_account
        message['Subject'] = '[Calamari Alert Service]'
        message.attach(MIMEText(content))
        try:
            mail_server = smtplib.SMTP(self.domain_name, self.port)
            mail_server.ehlo()
            mail_server.starttls()
            mail_server.ehlo()
            mail_server.login(self.user, self.password)
            mail_server.sendmail(self.user, to_account, message.as_string())
            mail_server.close()
            logs.manager(logs.INFO, "EMAIL - Successfully sent email")
        except smtplib.SMTPException:
            logs.manager(logs.ERROR, "EMAIL - unable to send email")
