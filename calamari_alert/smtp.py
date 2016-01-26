import smtplib
from calamari_alert.common import logs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SMTPClient(object):

    def __init__(self, user, password, domain_name, port):
        self.mode = None
        self.user = user
        self.password = password
        self.domain_name = domain_name
        self.port = port

    def set_mode(self, mode):
        self.mode = mode

    def sent(self, to_account, content):
        message = MIMEMultipart()
        message['From'] = self.user
        message['To'] = to_account
        message['Subject'] = '[Calamari Alert Service]'
        message.attach(MIMEText(content))
        try:
            mail_server = smtplib.SMTP(self.domain_name, self.port)
            mail_server.ehlo()

            if self.mode == 'TLS':
                mail_server.starttls()

            mail_server.login(self.user, self.password)
            mail_server.sendmail(self.user, to_account, message.as_string())
            mail_server.close()
            logs.manager(logs.INFO, "EMAIL - Successfully sent email")
            return True
        except smtplib.socket.gaierror:
            logs.manager(logs.ERROR, "Couldn't contact the host")
        except smtplib.SMTPAuthenticationError:
            logs.manager(logs.ERROR, "Login failed")
        except Exception, msg:
            logs.manager(logs.ERROR, msg.message)
        return False