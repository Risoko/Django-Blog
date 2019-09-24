from email.message import EmailMessage
from typing import List
from smtplib import SMTP_SSL

from main_blog.settings import USER_EMAIL, PASSWORD_EMAIL 

def send_email(mail_from:str, mail_to:List[str], mail_subject:str, message:str):
    """
    Tool send email if it succeeds return True else False.
    """
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = mail_subject
    msg['From'] = mail_from
    msg['To'] = ', '.join(mail_to)
    try:
        serwer = SMTP_SSL('smtp.gmail.com', 465)
        serwer.ehlo()
        serwer.login(user=USER_EMAIL, password=PASSWORD_EMAIL)
        serwer.send_message(msg)
        serwer.quit()
    except Exception:
        return False
    else:
        return True


