import smtplib
import os
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(user, pwd, recipient, subject, body):
        gmail_user = user
        gmail_pwd  = pwd
        FROM = user
        TO = recipient if type(recipient) is list else [recipient]
        
        #TEST
        msg = MIMEMultipart('alternative')
        msg['SUBJECT'] = subject
        msg['FROM'] = user
        msg['TO'] = recipient

        #prepare message - new
        part1 = MIMEText(body, 'plain')
        part2 = MIMEText(body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls() 
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, msg.as_string())
                server.close()
        except:
                pass
        # What do if can't send email?
