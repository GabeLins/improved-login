from secrets import token_urlsafe
from argparse import ArgumentParser
import os

path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(path, 'LoginSystem/data')
key_path = os.path.join(path, 'server.key')

parser = ArgumentParser(description='Flask login application.')

parser.add_argument(
    '-i', '--host', type=str, 
    help='Specifies the server IP address', 
    default='0.0.0.0'
)
parser.add_argument(
    '-p', '--port', type=int,
    help='Specifies the server connection port',
    default=80
)
parser.add_argument(
    '-k', '--key', type=str, 
    help='Specifies a server SECRET_KEY',
    default=token_urlsafe(32)
)
parser.add_argument(
    '-s', '--force-ssl', action='store_const', 
    help='Forces SSL encryption', dest='ssl',
    const=('server.crt', 'server.key')
)
parser.add_argument(
    '-d', '--debug', action='store_true',
    help='Run server in debug mode'
)


if __name__ == '__main__':
    args = parser.parse_args()

    with open(os.path.join(path, 'secret.txt'), 'w+') as key:
        key.write(args.key)

    # Import modules
    from LoginSystem.security import generate_ssl
    from LoginSystem import app, db

    if ( not os.path.exists(db_path) ):
        os.mkdir(db_path)

    if ( args.ssl and not os.path.exists(key_path) ):
        generate_ssl()

    print(f' * Server SECRET_KEY: {app.config["SECRET_KEY"]}')
    
    db.create_all(app=app)
    app.run(args.host, args.port, debug=args.debug, ssl_context=args.ssl)
