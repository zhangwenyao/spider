import smtplib
from email.mime.text import MIMEText
from logging.handlers import SMTPHandler


class Mail(SMTPHandler):

    def emit(self, record):
        try:
            server = smtplib.SMTP(self.mailhost, self.mailport)
            server.starttls()  # for tls add this line
            server.login(self.username, self.password)
            msg = MIMEText(self.format(record), 'html')
            msg['Subject'] = self.subject
            msg['From'] = self.fromaddr
            msg['To'] = ','.join(self.toaddrs)
            server.send_message(msg)
            server.quit()
        except Exception:
            self.handleError(record)
