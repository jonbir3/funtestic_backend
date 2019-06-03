from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import email
import os
from funtestic_backend.settings import BASE_DIR

FROM_USER = 'funtesticofficial@gmail.com'
MAIL_PASSWORD = os.environ.get('FROM_USER_PASSWORD')
if MAIL_PASSWORD is None:
    raise ValueError('MAIL_PASSWORD in utilities must be exported as variant variable')


def send_mail(subject, body, to_user, pdf_name=None):
    # subject = 'Report for child - Funtestic'
    # body = 'Hi! We sent you a report for your child.'
    msg = MIMEMultipart()
    msg['From'] = FROM_USER
    msg['To'] = to_user
    msg['Subject'] = subject
    rcpt = to_user
    if pdf_name:
        report = BASE_DIR + '/media/' + pdf_name
        fo = open(report, 'rb')
        attach = email.mime.application.MIMEApplication(fo.read(), _subtype="pdf")
        fo.close()
        attach.add_header('Content-Disposition', 'attachment', filename=report)
        msg.attach(attach)
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(msg['From'], MAIL_PASSWORD)
    server.sendmail(msg['From'], rcpt, msg.as_string())
    server.quit()
