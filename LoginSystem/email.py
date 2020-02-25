# Application Settings
from LoginSystem import settings as sets

# Email and Connection Modules
from email.headerregistry import Address
from email.message import EmailMessage
from secrets import token_urlsafe
import os.path
import smtplib


# This function is responsible for sending verification tokens to the user
def send_mail ( domain: tuple, token: str, target: str, endpoint: str ):
    # Create a link with the domain name and the endpoint + token
    link = os.path.join(domain[0], f'{endpoint}/{token}')

    # Create a random one-use email address
    sender = Address('Login No-Reply', token_urlsafe(24), domain[1])

    # Open an email template for the specified endpoint
    with open(f'emails/{endpoint}.html', 'r') as body:
        message = EmailMessage()
        message.add_alternative(
            body.read().replace('#[LINK]#', link),
            subtype='html'
        )

    # Write the email message headers
    message['Subject'] = {
        'reset': 'Password Recovery',
        'verify': 'Verify Account'
    }[endpoint]
    message['From'] = sender
    message['To'] = target

    # Connect to a SMTP server and send the message
    with smtplib.SMTP(sets['email_server'], sets['email_port']) as smtp:
        smtp.login(
            sets['email_username'], sets['email_password']
        )
        smtp.send_message(message)
