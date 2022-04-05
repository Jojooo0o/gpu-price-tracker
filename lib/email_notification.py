import smtplib
from email.mime.text import MIMEText
import config as cfg
from lib.contact import Contact


TEXT_SUBTYPE = 'plain'


def send_notification(mailserver, sender_port, data):
    '''
    Function handling smtp and message sending.
    '''
    try:
        # Create SMTP Session
        smtp = smtplib.SMTP(mailserver, port=sender_port)

        # Start TLS
        smtp.starttls()

        # Authenticate user
        smtp.login(cfg.EMAIL_USERNAME, cfg.EMAIL_PASSWORD)

        # Define Message
        msg=msg_wrapper(data.sender, data.receiver, data.subject, data.content)
        
        # Send Mail
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())

        # Terminate Session
        smtp.quit()
        print('Email sent successfully')

    except Exception as ex:
        print('Email sending failed: ', ex)


def msg_wrapper(sender:Contact, receiver:Contact, subject:str, body:str):
    '''
    Defines info / contents for each individual message
    '''
    content = f'''\
               {body}
            '''

    msg = MIMEText(content, TEXT_SUBTYPE)
    msg['Subject'] = subject
    msg['From'] = sender.email
    msg['To'] = receiver.email

    return msg
