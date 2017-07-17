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
        SUBJECT = subject
        TEXT = body
        
        #TEST
        msg = MIMEMultipart('alternative')
        msg['SUBJECT'] = subject
        msg['FROM'] = user
        msg['TO'] = recipient
        text = body
        #not reliable, depending on where everything is in file tree (so only works in my system)
        fp = open(os.path.join(sys.path[0],'protocat/templates/password_reset_email.html'))
        
        html = """
        <html>
                <head></head>
                <body>
                        <p>
                                <h2>Hi!</h2><br>
                                How are you?<br>
                                Here is the <a href="http://www.python.org">link</a> you wanted.
                        </p>
                </body>
        </html>
        """
        #END TEST
        
        #prepare message - old
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

        #prepare meddage - new
        part1 = MIMEText(text, 'plain')
        #part2 = MIMEText(html, 'html') -old
        part2 = MIMEText(fp.read(), 'html')
        fp.close()
        msg.attach(part1)
        msg.attach(part2)
        
        try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls() 
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message) #old
                server.sendmail(FROM, TO, msg.as_string()) #new
                server.close()
        except:
                pass
        # What do if can't send email?
