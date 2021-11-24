import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os, json
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
# secret 설정
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

class Util:
    @staticmethod
    def send_email(data):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(get_secret("EMAIL_HOST_USER"), get_secret("EMAIL_HOST_PASSWORD"))

        mail_html = "<html>" \
                    "<body>" + data['email_body']+\
                    "</body>" \
                    "</html>"
        mail_html = MIMEText(mail_html, 'html')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = data['email_subject']
        msg['From'] = get_secret("EMAIL_HOST_USER")
        msg['To'] = data['to_email']
        msg.attach(mail_html)

        server.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
        server.quit()
