from LoginSystem.security import *
from LoginSystem import app, db
import os

path = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(path, 'LoginSystem/data')
configs_path = os.path.join(path, 'app.cfg')
cert_path = os.path.join(path, 'server.key')

def setup ():
    port = 80
    if ( not os.path.exists(database_path) ):
        os.mkdir(database_path)

    if ( not os.path.exists(configs_path) ):
        generate_secret_key(configs_path)

    if ( not os.path.exists(cert_path) ):
        use_ssl = input('Use a SSL Certificate? (Y/n): ').lower() or 'y'
        if ( use_ssl == 'y' ):
            generate_certificate()
            port = 443

    return port


if __name__ == '__main__':
    port = setup()
    ctx = None
    
    app.config.from_pyfile(configs_path)
    db.create_all(app=app)
    if ( port == 443 ):
        ctx = ('server.crt', 'server.key')

    app.run('0.0.0.0', port, ssl_context=ctx)
