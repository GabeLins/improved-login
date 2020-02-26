from argparse import ArgumentParser
from secrets import token_urlsafe
import json

parser = ArgumentParser(description='Flask login application.')

parser.add_argument(
    '-i', '--host',
    help='Specify the server IP address',
    dest='server_addr', metavar='HOST'
)

parser.add_argument(
    '-p', '--port', type=int,
    help='Specify the server connection port',
    dest='server_port', metavar='PORT'
)

parser.add_argument(
    '-k', '--key', default=token_urlsafe(32),
    help='Specify the server SECRET_KEY',
    dest='secret_key', metavar='KEY'
)

parser.add_argument(
    '-s', '--force-ssl', action='store_const', 
    help='Force SSL encryption', dest='ssl',
    const=('server.crt', 'server.key')
)

parser.add_argument(
    '-d', '--debug', action='store_true',
    help='Run server in debug mode'
)

parser.add_argument(
    '-S', '--smtp-host',
    help='Specify the SMTP server address',
    dest='email_server', metavar='HOST'
)

parser.add_argument(
    '-P', '--smtp-port', type=int,
    help='Specify the SMTP server port',
    dest='email_port', metavar='PORT'
)

parser.add_argument(
    '-U', '--smtp-user',
    help='Specify the SMTP server username',
    dest='email_username', metavar='USER'
)

parser.add_argument(
    '-K', '--smtp-pass',
    help='Specify the SMTP server password',
    dest='email_password', metavar='PASS' 
)


def setup ():
    try:
        # Attempt to load settings file
        with open('settings.json', 'r') as setup_file:
            settings = json.load(setup_file)
    except FileNotFoundError:
        # Generate a settings dictionary using this default settings:
        settings = {
            'secret_key': 'SECRET_KEY',
            'server_addr': '0.0.0.0',
            'server_port': 80,
            'email_server': 'localhost',
            'email_port': 2525,
            'email_username': None,
            'email_password': None
        }

    # Parse the command-line arguments into a dictionary
    args = parser.parse_args()
    _args = dict(args.__dict__)

    # Generate a new settings dictionary using the command-line keys
    for key in settings:
        if ( key == 'email_templates' ): continue
        settings[key] = _args[key] or settings[key]
    
    # Store the new settings data in the settings.json file
    with open('settings.json', 'w') as setup_file:
        json.dump(settings, setup_file, indent=4)
    
    return args
