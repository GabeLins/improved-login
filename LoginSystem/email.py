from email.headerregistry import Address
from email.message import EmailMessage
from secrets import token_urlsafe
import os.path
import smtplib

def send_token ( domain, token, target ):
    link = os.path.join(domain[0], f'reset/{token}')
    sender = f'{token_urlsafe(32)}@{domain[1]}'

    with open('TEMPLATE', 'r') as body:
        message = EmailMessage()
        message.add_alternative(
            body.read().replace('#[LINK]#', link),
            subtype='html'
        )

    message['Subject'] = 'Password Recovery'
    message['From'] = sender
    message['To'] = target

    with smtplib.SMTP('SMTP-SERVER', 25) as server:
        server.login('USERNAME', 'PASSWORD')
        server.send_message(message)