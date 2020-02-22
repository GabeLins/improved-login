from LoginSystem import settings as sets
from email.headerregistry import Address
from email.message import EmailMessage
from secrets import token_urlsafe
import os.path
import smtplib

def mail_recover ( domain, token, target ):
    link = os.path.join(domain[0], f'reset/{token}')
    sender = Address('Login No-Reply', token_urlsafe(24), domain[1])

    with open('emails/recover.html', 'r') as body:
        message = EmailMessage()
        message.add_alternative(
            body.read().replace('#[LINK]#', link),
            subtype='html'
        )

    message['Subject'] = 'Password Recovery'
    message['From'] = sender
    message['To'] = target

    with smtplib.SMTP(sets['email_server'], sets['email_port']) as smtp:
        smtp.login(
            sets['email_username'], sets['email_password']
        )
        smtp.send_message(message)
